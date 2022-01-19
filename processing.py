import json
import pandas as pd
import feature_extraction
import nltk
import time
from abc import ABC, abstractmethod

class Sequencer: 
    def __init__(self, operations=None, verbose=None):
        if operations is None:
            self.seq = []
        elif isinstance(operations, (list, tuple)):
            self.seq = operations
        else:
            self.seq = [operations]
            
        self.verbose = verbose
        self.time_taken = 0
            
    def add_operation(self, op, index=None):
        if index is None:
            self.seq.append(op)
        else:
            self.seq = self.seq[:index] + [op] + self.seq[index:]
            
    def __call__(self, data):        
        for i, op in enumerate(self.seq, 1):
            start = time.time()
            print(f'Step {i}/{len(self.seq)} ({op}) in progress', flush=True)

            data = op(data)
            time_taken = time.time() - start
            self.time_taken += time_taken
            print(f'Step {i}/{len(self.seq)} ({op}) completed, time elapsed: {time_taken} seconds\n')
        
        print(f'Finished processing. Total time taken: {self.time_taken}')
        return data
    
class Operation(ABC):
    
    @abstractmethod
    def __call__(self, **kwargs):
        pass
    
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class LoadJson(Operation):
    def __init__(self, encoding=None):
        super().__init__()
        self.encoding = encoding
        
    def __call__(self, path):
        with open(path, 'r', encoding=self.encoding) as f:
            data = json.load(f)
        return data
    
class DictToDF(Operation):
    def __init__(self, numeric_cols=None):
        super().__init__()
        if numeric_cols is None:
            self.numeric_cols = []
        else:
            self.numeric_cols = numeric_cols
        
    def __call__(self, d):
        try:
            df = pd.DataFrame(d)
        except ValueError:
            df = pd.DataFrame([d])
            
        for col in self.numeric_cols:
            df[col] = df[col].str.replace(',', '').astype(float)

        return df
    
class DropColumns(Operation):
    def __init__(self, drop_cols):
        super().__init__()
        self.drop_cols = drop_cols

    def __call__(self, df):
        df = df.drop(columns=self.drop_cols)

        return df
    
class FillNoneValues(Operation):
    def __init__(self, to_cols=None, replace_null_with=''):
        super().__init__()
        self.to_cols = to_cols
        self.replace_null_with = replace_null_with
        
    def __call__(self, df):
        columns = self.to_cols
        if columns is None:
            columns = df.columns
        
        for col in columns:
            mask = df[col].isnull()
            df.loc[mask, col] = df.loc[mask, col] = self.replace_null_with    

        return df
    
class ApplyFunctionToColumns(Operation):
    def __init__(self, func, *args, to_cols=None, to_series=False,
                 to_dtype=None, concat_axis=1, min_occurances=None, **kwargs):
        super().__init__()
        
        self.func = func
        self.to_cols = to_cols
        self.to_series =to_series
        self.to_dtype = to_dtype
        self.concat_axis = concat_axis
        if args is None:
            self.args = tuple()
        else:
            self.args = args
        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs
        
        self.min_occurances = min_occurances
        
    def __call__(self, df):
        columns = self.to_cols
        if columns is None:
            columns = df.columns
            
        l = []
        for col in columns:
            results = df[col].apply(self.func, *self.args, **self.kwargs)
            if self.to_series:
                results = results.apply(pd.Series)
            if self.to_dtype is not None:
                results = results.astype(self.to_dtype)
            results.columns = [col + '_' + colname for colname in results.columns]
                
            if self.min_occurances is not None:
                results = results.loc[:, results.sum(axis=0) > self.min_occurances]
                
            l.append(results)
        df = pd.concat([df, *l], axis=self.concat_axis)
        
        return df
    
class FilterColumnsByStd(Operation):
    def __init__(self, min_std=None, max_std=None):
        super().__init__()
        assert (min_std is not None) or (max_std is not None)
        self.min_std = min_std
        self.max_std = max_std


    def __call__(self, df):
        mask_above_min, mask_below_max = True, True
        if self.min_std is not None:
            mask_above_min = df.std() > self.min_std
        if self.max_std is not None:
            mask_below_max = df.std() > self.min_std
        
        mask = mask_above_min & mask_below_max
        non_numeric_cols_mask = pd.Series({col: True for col in df.columns if col not in mask.index})
        mask = mask.append(non_numeric_cols_mask)
        
        n_columns = len(df.columns)
        print(f'Got {n_columns} columns in DataFrame')
        df = df.loc[:, mask]
        print(f'Dropped {n_columns - len(df.columns)} columns in DataFrame')

        return df
    
class ApplyFunctionToRows(Operation):
    def __init__(self, func, *args, disregard_columns=None, to_series=False,
                 to_dtype=None, concat_axis=1, **kwargs):
        super().__init__()
        
        self.func = func
        self.to_series = to_series
        if disregard_columns is None:
            self.disregard_columns = []
        else:
            self.disregard_columns = disregard_columns
        self.to_dtype = to_dtype
        self.concat_axis = concat_axis
        if args is None:
            self.args = tuple()
        else:
            self.args = args
        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs
        
    def __call__(self, df):
        
        columns = [col for col in df.columns if col not in self.disregard_columns and pd.api.types.is_numeric_dtype(df[col])]
        results = df[columns].apply(self.func, axis=1, *self.args, **self.kwargs)
        if self.to_series:
            results = results.apply(pd.Series)
        if self.to_dtype is not None:
            results = results.astype(self.to_dtype)

        df = pd.concat([df, results], axis=self.concat_axis)
        
        return df
    
class SaveToCsv(Operation):
    def __init__(self, path):
        self.path = path
        
    def __call__(self, df):
        df.to_csv(self.path, index=0)
        return df
    
if __name__ == '__main__':
    MIN_POS_IN_CORPUS = 100
    MIN_NER_IN_CORPUS = 20
    path = 'products.json'
    output_path = 'dataset.csv'
    text_columns = ['desc_text', 'title']
    
    seq = Sequencer([
        LoadJson(encoding='utf-8'),
        DictToDF(numeric_cols=['rating', 'rating_count', 'photos_count']),
        DropColumns(drop_cols=['url', 'desc']),
        FillNoneValues(to_cols=text_columns, replace_null_with=''),
        ApplyFunctionToColumns(feature_extraction.get_main_stats,
                               to_cols=text_columns,
                               to_series=True,
                               to_dtype=float,
                               concat_axis=1
                               ),
        FilterColumnsByStd(min_std=0.0),
        ApplyFunctionToRows(
            feature_extraction.get_ratios,
            disregard_columns=text_columns + ['rating', 'rating_count'],
            to_series=True,
            to_dtype=float,
            concat_axis=1
            ),
        ApplyFunctionToColumns(feature_extraction.get_pos_features,
                               to_cols=text_columns,
                               to_series=True,
                               to_dtype=float,
                               concat_axis=1,
                               min_occurances=MIN_POS_IN_CORPUS
                               ),
        ApplyFunctionToColumns(feature_extraction.get_ner_tag_counts,
                               to_cols=text_columns,
                               to_series=True,
                               to_dtype=float,
                               concat_axis=1,
                               min_occurances=MIN_NER_IN_CORPUS
                               ),
        FillNoneValues(replace_null_with=0),
        DropColumns(drop_cols=text_columns),
        SaveToCsv('dataset.csv')
        ])
    
    df = seq(path)

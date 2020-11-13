import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def multi_analyze(raw_data, params):
    pd_data = pd.DataFrame(raw_data)
    columns = pd_data.columns
    assert('time' in columns)
    formula = "time~ "
    for i in range(len(params)):
        assert(params[i] in columns)
        formula = formula + f" {params[i]} "
        if i<len(params)-1:
            formula = formula + "+"
    anova_results = anova_lm(ols(formula,pd_data).fit())
    print("====================== anova analyze report =======================")
    print(anova_results)
    print(" ")

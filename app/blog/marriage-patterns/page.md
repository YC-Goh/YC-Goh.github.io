#   Marriage Patterns in Singapore

Some analyses for fun.
I am not a specialised analyst of the marriage market.


```python
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt
import seaborn as sns
from _0_get_datasets_list import DatasetsList
import matplotlib_inline
matplotlib_inline.backend_inline.set_matplotlib_formats('svg')
```

Questions that interest me when it comes to marriage patterns:
1.  Associative matching:
    -   Are highly educated people matching other highly educated people?
    -   Are high-income people matching other high-income people?
    -   Are people matching with others of similar age?
    -   Are associative matching patterns changing over time?
2.  Relative success rates:
    -   What are the transition rates between Singlehood and Marriage?
    -   How do transition rates differ by age, education level, and income level?
    -   How do transition rates differ by cohort?
    -   How have transition rates changed over the years?
3.  Inferences about the state of the marriage market:
    -   What do patterns of associative matching and relative success rates tell us about how matching is happening?
    -   What do the matching patterns suggest to be weaknesses in the dating and marriage market?
    -   In the decomposition of the sources of low fertility, do dating and marriage patterns contribute significantly to low fertility? Or are the sources more located in the economic realm?

Load datasets list


```python
datasets = DatasetsList('../data/datasets.csv')
```

##  1.  Marriage Patterns

### A.  Marriages by Qualification


```python
datasets.search([r'(?i:marriage)', r'(?i:\bqual)', r'(?i:muslim)'], [False, False, True])
```

    {
      "d_235cda81c98c02c8fe2e6d86dab461f0": "Marriages Under The Women's Charter By Educational Qualification Of Grooms And Brides, Annual",
      "d_988d10c7d86fd052fd28f286d9454eed": "Median Age At First Marriage Of Grooms And Brides Married Under The Women's Charter By Educational Qualification, Annual",
      "d_f9cc6b55334da7fba42dc0e2a7be6aee": "First Marriages For Couples Under The Women's Charter By Educational Qualification Of Grooms And Brides, Annual",
      "d_e1149657519492ba9928a7afb27d442e": "Median Age At First Marriage Of Grooms And Brides By Educational Qualification, Annual",
      "d_a972c0c752ca2aab0d1bd6466cde9149": "Inter-Ethnic Marriages Under The Women's Charter By Educational Qualification Of Grooms And Brides, Annual"
    }


Load the marriages by education qualification dataset and reshape it to make sense.


```python
df_m = datasets.retrieve_dataset('d_235cda81c98c02c8fe2e6d86dab461f0')
df_m = df_m.sort_values(by=['_id'])
df_m['Brides'] = df_m['DataSeries'].str.extract(r'(?i:brides?\W+\b(.+)\b)', expand=True).ffill()
df_m['Grooms'] = df_m['DataSeries'].str.extract(r'(?i:grooms?\W+\b(.+)\b)', expand=True)
df_m = df_m.dropna(subset=['Brides', 'Grooms'], how='any')
df_m = df_m.drop(columns=['_id', 'DataSeries'])
df_m[['Brides', 'Grooms']] = df_m[['Brides', 'Grooms']].replace(r'.*(?i:sec.*below).*', 'Pri/Sec', regex=True)
df_m[['Brides', 'Grooms']] = df_m[['Brides', 'Grooms']].replace(r'.*(?i:post.*sec.*).*', 'Diploma', regex=True)
df_m[['Brides', 'Grooms']] = df_m[['Brides', 'Grooms']].replace(r'.*(?i:univ.*).*', 'Degree', regex=True)
df_m['Brides'] = pd.Categorical(df_m['Brides'], categories=['Pri/Sec', 'Diploma', 'Degree'], ordered=True)
df_m['Grooms'] = pd.Categorical(df_m['Grooms'], categories=['Pri/Sec', 'Diploma', 'Degree'], ordered=True)
df_m = df_m.set_index(keys=['Brides', 'Grooms'], append=False)
df_m = df_m.rename_axis(columns=['Year'])
df_m = df_m.transpose().sort_index(axis=0).sort_index(axis=1)
df_m
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Brides</th>
      <th colspan="3" halign="left">Pri/Sec</th>
      <th colspan="3" halign="left">Diploma</th>
      <th colspan="3" halign="left">Degree</th>
    </tr>
    <tr>
      <th>Grooms</th>
      <th>Pri/Sec</th>
      <th>Diploma</th>
      <th>Degree</th>
      <th>Pri/Sec</th>
      <th>Diploma</th>
      <th>Degree</th>
      <th>Pri/Sec</th>
      <th>Diploma</th>
      <th>Degree</th>
    </tr>
    <tr>
      <th>Year</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1984</th>
      <td>14137</td>
      <td>1966</td>
      <td>561</td>
      <td>865</td>
      <td>1015</td>
      <td>468</td>
      <td>72</td>
      <td>145</td>
      <td>743</td>
    </tr>
    <tr>
      <th>1985</th>
      <td>12887</td>
      <td>1809</td>
      <td>533</td>
      <td>832</td>
      <td>946</td>
      <td>435</td>
      <td>81</td>
      <td>154</td>
      <td>818</td>
    </tr>
    <tr>
      <th>1986</th>
      <td>10545</td>
      <td>1484</td>
      <td>407</td>
      <td>688</td>
      <td>804</td>
      <td>413</td>
      <td>85</td>
      <td>133</td>
      <td>816</td>
    </tr>
    <tr>
      <th>1987</th>
      <td>12473</td>
      <td>1880</td>
      <td>537</td>
      <td>902</td>
      <td>1002</td>
      <td>531</td>
      <td>103</td>
      <td>203</td>
      <td>1004</td>
    </tr>
    <tr>
      <th>1988</th>
      <td>12709</td>
      <td>2087</td>
      <td>588</td>
      <td>1011</td>
      <td>1255</td>
      <td>542</td>
      <td>134</td>
      <td>246</td>
      <td>1210</td>
    </tr>
    <tr>
      <th>1989</th>
      <td>11710</td>
      <td>1950</td>
      <td>569</td>
      <td>973</td>
      <td>1184</td>
      <td>564</td>
      <td>133</td>
      <td>264</td>
      <td>1199</td>
    </tr>
    <tr>
      <th>1990</th>
      <td>11544</td>
      <td>2109</td>
      <td>634</td>
      <td>1050</td>
      <td>1323</td>
      <td>670</td>
      <td>173</td>
      <td>279</td>
      <td>1409</td>
    </tr>
    <tr>
      <th>1991</th>
      <td>11393</td>
      <td>2170</td>
      <td>657</td>
      <td>1269</td>
      <td>1628</td>
      <td>688</td>
      <td>203</td>
      <td>323</td>
      <td>1654</td>
    </tr>
    <tr>
      <th>1992</th>
      <td>11574</td>
      <td>2358</td>
      <td>661</td>
      <td>1386</td>
      <td>1875</td>
      <td>774</td>
      <td>209</td>
      <td>359</td>
      <td>1829</td>
    </tr>
    <tr>
      <th>1993</th>
      <td>10702</td>
      <td>2273</td>
      <td>681</td>
      <td>1594</td>
      <td>1857</td>
      <td>880</td>
      <td>241</td>
      <td>400</td>
      <td>2064</td>
    </tr>
    <tr>
      <th>1994</th>
      <td>9903</td>
      <td>2234</td>
      <td>648</td>
      <td>1715</td>
      <td>1960</td>
      <td>905</td>
      <td>300</td>
      <td>452</td>
      <td>2126</td>
    </tr>
    <tr>
      <th>1995</th>
      <td>9200</td>
      <td>2145</td>
      <td>696</td>
      <td>1853</td>
      <td>2164</td>
      <td>1051</td>
      <td>297</td>
      <td>517</td>
      <td>2630</td>
    </tr>
    <tr>
      <th>1996</th>
      <td>8503</td>
      <td>1990</td>
      <td>623</td>
      <td>1778</td>
      <td>2119</td>
      <td>1147</td>
      <td>301</td>
      <td>555</td>
      <td>2919</td>
    </tr>
    <tr>
      <th>1997</th>
      <td>8433</td>
      <td>2072</td>
      <td>709</td>
      <td>1916</td>
      <td>2412</td>
      <td>1325</td>
      <td>348</td>
      <td>652</td>
      <td>3433</td>
    </tr>
    <tr>
      <th>1998</th>
      <td>7260</td>
      <td>1771</td>
      <td>664</td>
      <td>1706</td>
      <td>2042</td>
      <td>1165</td>
      <td>372</td>
      <td>644</td>
      <td>3347</td>
    </tr>
    <tr>
      <th>1999</th>
      <td>7547</td>
      <td>1850</td>
      <td>675</td>
      <td>1987</td>
      <td>2443</td>
      <td>1488</td>
      <td>426</td>
      <td>851</td>
      <td>4294</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>6001</td>
      <td>1441</td>
      <td>611</td>
      <td>1607</td>
      <td>2104</td>
      <td>1363</td>
      <td>415</td>
      <td>789</td>
      <td>4219</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>5702</td>
      <td>1435</td>
      <td>625</td>
      <td>1629</td>
      <td>2093</td>
      <td>1276</td>
      <td>438</td>
      <td>912</td>
      <td>4168</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>5101</td>
      <td>1386</td>
      <td>702</td>
      <td>1701</td>
      <td>2457</td>
      <td>1462</td>
      <td>551</td>
      <td>1066</td>
      <td>4831</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>4277</td>
      <td>1192</td>
      <td>587</td>
      <td>1554</td>
      <td>2406</td>
      <td>1472</td>
      <td>496</td>
      <td>1105</td>
      <td>5002</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>4105</td>
      <td>1348</td>
      <td>573</td>
      <td>1272</td>
      <td>2793</td>
      <td>1380</td>
      <td>458</td>
      <td>1164</td>
      <td>4998</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>4494</td>
      <td>1493</td>
      <td>602</td>
      <td>1438</td>
      <td>2818</td>
      <td>1430</td>
      <td>485</td>
      <td>1289</td>
      <td>4993</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>4086</td>
      <td>1500</td>
      <td>558</td>
      <td>1408</td>
      <td>3040</td>
      <td>1486</td>
      <td>538</td>
      <td>1471</td>
      <td>5674</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>3812</td>
      <td>1329</td>
      <td>598</td>
      <td>1353</td>
      <td>2983</td>
      <td>1511</td>
      <td>598</td>
      <td>1582</td>
      <td>6087</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>3656</td>
      <td>1420</td>
      <td>572</td>
      <td>1189</td>
      <td>3005</td>
      <td>1549</td>
      <td>622</td>
      <td>1740</td>
      <td>6636</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>3643</td>
      <td>1535</td>
      <td>624</td>
      <td>1296</td>
      <td>3181</td>
      <td>1682</td>
      <td>638</td>
      <td>2007</td>
      <td>7454</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>3228</td>
      <td>1277</td>
      <td>611</td>
      <td>982</td>
      <td>2639</td>
      <td>1608</td>
      <td>625</td>
      <td>1891</td>
      <td>7369</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>3391</td>
      <td>1327</td>
      <td>670</td>
      <td>1117</td>
      <td>2984</td>
      <td>1766</td>
      <td>732</td>
      <td>2129</td>
      <td>8724</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>3353</td>
      <td>1355</td>
      <td>593</td>
      <td>1094</td>
      <td>3037</td>
      <td>1787</td>
      <td>755</td>
      <td>2211</td>
      <td>8949</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>2469</td>
      <td>1159</td>
      <td>622</td>
      <td>963</td>
      <td>2666</td>
      <td>1704</td>
      <td>743</td>
      <td>2114</td>
      <td>8740</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>2402</td>
      <td>1196</td>
      <td>627</td>
      <td>974</td>
      <td>2943</td>
      <td>1680</td>
      <td>760</td>
      <td>2490</td>
      <td>9791</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>2113</td>
      <td>1160</td>
      <td>505</td>
      <td>1024</td>
      <td>3147</td>
      <td>1848</td>
      <td>642</td>
      <td>2490</td>
      <td>9615</td>
    </tr>
    <tr>
      <th>2016</th>
      <td>1954</td>
      <td>1122</td>
      <td>427</td>
      <td>1008</td>
      <td>3021</td>
      <td>1714</td>
      <td>599</td>
      <td>2475</td>
      <td>9697</td>
    </tr>
    <tr>
      <th>2017</th>
      <td>1704</td>
      <td>966</td>
      <td>431</td>
      <td>880</td>
      <td>2895</td>
      <td>1809</td>
      <td>542</td>
      <td>2581</td>
      <td>10354</td>
    </tr>
    <tr>
      <th>2018</th>
      <td>1515</td>
      <td>893</td>
      <td>422</td>
      <td>798</td>
      <td>2626</td>
      <td>1679</td>
      <td>564</td>
      <td>2494</td>
      <td>10317</td>
    </tr>
    <tr>
      <th>2019</th>
      <td>1406</td>
      <td>831</td>
      <td>381</td>
      <td>795</td>
      <td>2407</td>
      <td>1537</td>
      <td>516</td>
      <td>2277</td>
      <td>9739</td>
    </tr>
    <tr>
      <th>2020</th>
      <td>958</td>
      <td>575</td>
      <td>276</td>
      <td>650</td>
      <td>2042</td>
      <td>1271</td>
      <td>370</td>
      <td>1993</td>
      <td>8989</td>
    </tr>
    <tr>
      <th>2021</th>
      <td>1325</td>
      <td>737</td>
      <td>314</td>
      <td>798</td>
      <td>2631</td>
      <td>1562</td>
      <td>497</td>
      <td>2563</td>
      <td>11674</td>
    </tr>
    <tr>
      <th>2022</th>
      <td>1467</td>
      <td>748</td>
      <td>392</td>
      <td>876</td>
      <td>2775</td>
      <td>1730</td>
      <td>530</td>
      <td>2677</td>
      <td>12180</td>
    </tr>
  </tbody>
</table>
</div>



Basic statistics:
1.  Proportion Equal-Level Marriages.
2.  Proportion Bride > Groom Marriages.
3.  Proportion of Groom qualification levels by Bride qualification levels.
4.  Proportion of Bride qualification levels by Groom qualification levels.


```python
df_m_p = df_m.div(df_m.sum(axis=1), axis=0).mul(100).copy(deep=True)
plt.figure(figsize=(9, 6))
plt.plot(df_m_p)
plt.legend([f'B: {b}; G: {g}' for b, g in df_m_p.columns.to_flat_index()], loc=9)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_12_0.svg)
    



```python
df_m_p_simp = pd.DataFrame.from_dict(
    {
        'Equal': df_m_p.loc[:,df_m_p.columns.get_level_values('Brides')==df_m_p.columns.get_level_values('Grooms')].sum(axis=1), 
        'Bride > Groom': df_m_p.loc[:,df_m_p.columns.get_level_values('Brides')>df_m_p.columns.get_level_values('Grooms')].sum(axis=1), 
        'Groom > Bride': df_m_p.loc[:,df_m_p.columns.get_level_values('Brides')<df_m_p.columns.get_level_values('Grooms')].sum(axis=1), 
    }, 
    orient='columns'
)
plt.figure(figsize=(9, 6))
plt.plot(df_m_p_simp)
plt.legend(df_m_p_simp.columns, loc=9)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_13_0.svg)
    



```python
df_m_p_b = df_m.stack(level=['Grooms'], future_stack=True).copy(deep=True)
if not isinstance(df_m_p_b, pd.DataFrame):
    df_m_p_b = df_m_p_b.to_frame()
df_m_p_b = df_m_p_b.div(df_m_p_b.groupby(by=['Year']).sum()).mul(100)
_, axs = plt.subplots(1, 3, figsize=(12,3), sharey=True)
for i in range(3):
    sns.lineplot(data=df_m_p_b, x='Year', y=df_m_p_b.columns[i], hue='Grooms', ax=axs[i])
    axs[i].legend(title='Groom', loc=8, bbox_to_anchor=(0.5, 1), ncols=3, fontsize='x-small')
    axs[i].set_ylabel('Percent')
    axs[i].set_title(f'Bride: {df_m_p_b.columns[i]}', pad=36)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_14_0.svg)
    



```python
df_m_p_g = df_m.stack(level=['Brides'], future_stack=True).copy(deep=True)
if not isinstance(df_m_p_g, pd.DataFrame):
    df_m_p_g = df_m_p_g.to_frame()
df_m_p_g = df_m_p_g.div(df_m_p_g.groupby(by=['Year']).sum()).mul(100)
_, axs = plt.subplots(1, 3, figsize=(12,3), sharey=True)
for i in range(3):
    sns.lineplot(data=df_m_p_g, x='Year', y=df_m_p_g.columns[i], hue='Brides', ax=axs[i])
    axs[i].legend(title='Bride', loc=8, bbox_to_anchor=(0.5, 1), ncols=3, fontsize='x-small')
    axs[i].set_ylabel('Percent')
    axs[i].set_title(f'Groom: {df_m_p_g.columns[i]}', pad=36)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_15_0.svg)
    


In addition to basic statistics, we can run basic inferential tests:
1.  Association tests:\
    Basically the same intuition as the basic chi-square tests of association.\
    1 = perfect association, 0 = no association.\
    Which means that the test statistic can be interpreted as a scale.
2.  Correlation tests:\
    Difference from association tests is that the test statistic has a sign and the sign is meaningful.\
    1 = perfect positive association, 0 = no association, -1 = perfect negative association.\
    By definition, correlation tests can only be used on ordered variables (which we have here).


```python
def _contingency_association_test(data:pd.Series, method:str='pearson'):
    datamat = data.unstack(level='Grooms')
    assoctest = sps.contingency.association(datamat, method=method)
    return assoctest
sns.lineplot(df_m.apply(_contingency_association_test, axis=1))
plt.title('Association between Bride and Groom educational qualifications')
plt.ylabel('Pearson Association Coefficient')
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_17_0.svg)
    



```python
def _kendalltau_contingency(contingency_table:pd.Series|pd.DataFrame):
    if isinstance(contingency_table, pd.DataFrame):
        contingency_table = contingency_table.melt(ignore_index=False).set_index(keys=contingency_table.columns.names, append=True)['value']
    assert contingency_table.index.nlevels == 2, 'Works only on 2-dimensional contingency tables!'
    try:
        contingency_table = pd.to_numeric(contingency_table, downcast='integer', errors='raise')
    except:
        raise TypeError('Contingency Tables are count tables')
    assert pd.api.types.is_integer_dtype(contingency_table), ''
    contingency_table = contingency_table.repeat(contingency_table)
    contingency_table = contingency_table.index.to_frame(index=False)
    contingency_table = contingency_table.stack(future_stack=True).rank(method='min')
    contingency_table = contingency_table.unstack()
    result = sps.kendalltau(*contingency_table.to_numpy().T)
    return result.statistic
sns.lineplot(df_m.apply(_kendalltau_contingency, axis=1))
plt.title('Kendall-Tau correlation between Bride and Groom educational qualifications')
plt.ylabel('Kendall-Tau Correlation Coefficient')
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_18_0.svg)
    


There seem to be 2 main stories:
1.  Positive Assortative Matching:\
    The most common kind of marriage is between people with similar education levels.
    In fact the level of matching is above chance levels.
    Either, one can see that the by-groom-level and by-bride-level proportions cannot be true under independent matching since then the proportions will have to be identical for all levels of bride/groom education,
    or one can also see from the association and correlation tests that sorting in Singapore's marriage market exhibits very high positive sortation.
2.  Increasing womens' education levels:\
    First, with non-equal marriages, the proportion of marriages with higher bride qualifications increases while the proportion with higher groom qualification falls.
    Second, under the by-groom-qualification sub-plots, all cases of brides having lower qualification decrease over time while all cases of brides having higher qualification increase.

Over time, there is another interesting story:
1.  While positive assortative matching is high, it has not been increasing and may be trending down in recent years.

These trends together seemingly imply some structure to how the dating and marriage markets that has not changed substantially in the past 4 decades.

### B.  Marriages by Age Groups


```python
datasets.search([r'(?i:marriage)', r'(?i:\bage)', r'(?i:muslim)'], [False, False, True])
```

    {
      "d_1c7a6c900300410dfb723927da7b3636": "First Marriages For Brides Under The Women's Charter By Age Group Of Grooms And Brides, Annual",
      "d_9fe2e79545bc18d80a1ea5cde8aa8b24": "Marriages Under The Women's Charter By Age Group Of Grooms, Annual",
      "d_7e58d5b4e06fbb22d958ed13761aa8d0": "Marriages Under The Women's Charter By Age Group Of Brides, Annual",
      "d_e42526ed15108b310f9efe5077bca27a": "Divorces Under The Women's Charter By Age At Marriage Of Male And Female Divorcees, Annual",
      "d_4a6347a51983571d5a5ccfda425266ed": "Marriages Under The Women's Charter By Age Group Of Grooms And Brides, Annual",
      "d_6cba526492c2b80c855323165af4cc94": "Total Marriages By Age Differential Of Grooms To Brides And Marriage Order, Annual",
      "d_2a589767aadd5550f887fe0005b9ba7e": "Annulments Under The Women's Charter By Duration Of Marriage, Age Group And Sex, Annual",
      "d_3e90aefaff9a8ec5b7d9d39f8dd53306": "Divorces Under The Women's Charter By Age At Marriage, Ethnic Group And Sex Of Divorcees, Annual",
      "d_988d10c7d86fd052fd28f286d9454eed": "Median Age At First Marriage Of Grooms And Brides Married Under The Women's Charter By Educational Qualification, Annual",
      "d_65b0ae731eaff17df60af2dc62b5ca2f": "Marriages Under The Women's Charter By Age Group And Previous Marital Status Of Grooms, Annual",
      "d_48bab86448603efe0a6f0fcd6aa545b6": "Median Age At First Marriage Of Resident, Citizen Grooms And Brides, Annual",
      "d_04db3a4c50f93bc6a6a452b8e125bf78": "Median Age Of Grooms And Brides By Marriage Order, Annual",
      "d_2dd0a290d283c284d0513bd5e38c7ebb": "Median Age Of Grooms And Brides Married Under The Women's Charter By Marriage Order, Annual",
      "d_9799a59ff1a9037006366d2828a69111": "First Marriages For Couples Under The Women's Charter By Age Group Of Grooms And Brides, Annual",
      "d_e1149657519492ba9928a7afb27d442e": "Median Age At First Marriage Of Grooms And Brides By Educational Qualification, Annual",
      "d_f7569e58a97006324771bd94ab00e66d": "Marriages Under The Women's Charter By Age Group And Ethnic Group Of Grooms And Brides, Annual"
    }


Load the marriages by age groups dataset and reshape it to make sense.


```python
df_a = datasets.retrieve_dataset('d_4a6347a51983571d5a5ccfda425266ed')
df_a = df_a.sort_values(by=['_id'])
df_a['Brides'] = df_a['DataSeries'].str.extract(r'(?i:brides?\W+\b(.+)\b)', expand=True).ffill()
df_a['Grooms'] = df_a['DataSeries'].str.extract(r'(?i:grooms?\W+\b(.+)\b)', expand=True)
df_a = df_a.dropna(subset=['Brides', 'Grooms'], how='any')
df_a = df_a.drop(columns=['_id', 'DataSeries'])
df_a['Brides'] = df_a['Brides'].str.replace(r'(?i:aged?|years?)', '', regex=True).str.strip()
df_a['Brides'] = df_a['Brides'].str.replace(r'(?i:under)', '<', regex=True).str.strip()
df_a['Brides'] = df_a['Brides'].str.replace(r'(?i:\W+over)', '+', regex=True).str.strip()
df_a['Grooms'] = df_a['Grooms'].str.replace(r'(?i:aged?|years?)', '', regex=True).str.strip()
df_a['Grooms'] = df_a['Grooms'].str.replace(r'(?i:under)', '<', regex=True).str.strip()
df_a['Grooms'] = df_a['Grooms'].str.replace(r'(?i:\W+over)', '+', regex=True).str.strip()
df_a['Brides'] = pd.Categorical(df_a['Brides'], categories=['< 20', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+'], ordered=True)
df_a['Grooms'] = pd.Categorical(df_a['Grooms'], categories=['< 20', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+'], ordered=True)
df_a = df_a.set_index(keys=['Brides', 'Grooms'], append=False)
df_a = df_a.rename_axis(columns=['Year'])
df_a = df_a.transpose().sort_index(axis=0).sort_index(axis=1)
df_a
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Brides</th>
      <th colspan="10" halign="left">&lt; 20</th>
      <th>...</th>
      <th colspan="10" halign="left">60+</th>
    </tr>
    <tr>
      <th>Grooms</th>
      <th>&lt; 20</th>
      <th>20-24</th>
      <th>25-29</th>
      <th>30-34</th>
      <th>35-39</th>
      <th>40-44</th>
      <th>45-49</th>
      <th>50-54</th>
      <th>55-59</th>
      <th>60+</th>
      <th>...</th>
      <th>&lt; 20</th>
      <th>20-24</th>
      <th>25-29</th>
      <th>30-34</th>
      <th>35-39</th>
      <th>40-44</th>
      <th>45-49</th>
      <th>50-54</th>
      <th>55-59</th>
      <th>60+</th>
    </tr>
    <tr>
      <th>Year</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1983</th>
      <td>65</td>
      <td>811</td>
      <td>417</td>
      <td>48</td>
      <td>4</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1984</th>
      <td>49</td>
      <td>718</td>
      <td>350</td>
      <td>56</td>
      <td>9</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1985</th>
      <td>52</td>
      <td>671</td>
      <td>304</td>
      <td>44</td>
      <td>7</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1986</th>
      <td>47</td>
      <td>488</td>
      <td>242</td>
      <td>39</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1987</th>
      <td>46</td>
      <td>513</td>
      <td>241</td>
      <td>43</td>
      <td>5</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>12</td>
    </tr>
    <tr>
      <th>1988</th>
      <td>40</td>
      <td>451</td>
      <td>246</td>
      <td>54</td>
      <td>7</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
    </tr>
    <tr>
      <th>1989</th>
      <td>46</td>
      <td>418</td>
      <td>232</td>
      <td>55</td>
      <td>6</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1990</th>
      <td>56</td>
      <td>364</td>
      <td>274</td>
      <td>63</td>
      <td>4</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1991</th>
      <td>68</td>
      <td>321</td>
      <td>246</td>
      <td>66</td>
      <td>7</td>
      <td>6</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1992</th>
      <td>68</td>
      <td>341</td>
      <td>234</td>
      <td>76</td>
      <td>22</td>
      <td>6</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1993</th>
      <td>57</td>
      <td>276</td>
      <td>187</td>
      <td>74</td>
      <td>15</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1994</th>
      <td>55</td>
      <td>227</td>
      <td>154</td>
      <td>66</td>
      <td>14</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>2</td>
      <td>4</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1995</th>
      <td>45</td>
      <td>221</td>
      <td>143</td>
      <td>66</td>
      <td>14</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1996</th>
      <td>50</td>
      <td>231</td>
      <td>127</td>
      <td>45</td>
      <td>18</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>10</td>
    </tr>
    <tr>
      <th>1997</th>
      <td>41</td>
      <td>222</td>
      <td>103</td>
      <td>43</td>
      <td>13</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>1</td>
      <td>12</td>
    </tr>
    <tr>
      <th>1998</th>
      <td>50</td>
      <td>237</td>
      <td>152</td>
      <td>49</td>
      <td>17</td>
      <td>8</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1999</th>
      <td>60</td>
      <td>214</td>
      <td>148</td>
      <td>52</td>
      <td>16</td>
      <td>4</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>4</td>
      <td>9</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>67</td>
      <td>205</td>
      <td>136</td>
      <td>28</td>
      <td>9</td>
      <td>5</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>3</td>
      <td>9</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>71</td>
      <td>180</td>
      <td>120</td>
      <td>31</td>
      <td>18</td>
      <td>6</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>1</td>
      <td>4</td>
      <td>13</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>49</td>
      <td>155</td>
      <td>94</td>
      <td>32</td>
      <td>16</td>
      <td>7</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>40</td>
      <td>136</td>
      <td>66</td>
      <td>22</td>
      <td>11</td>
      <td>6</td>
      <td>4</td>
      <td>6</td>
      <td>2</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>29</td>
      <td>144</td>
      <td>64</td>
      <td>38</td>
      <td>19</td>
      <td>14</td>
      <td>6</td>
      <td>5</td>
      <td>2</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>17</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>37</td>
      <td>133</td>
      <td>64</td>
      <td>49</td>
      <td>36</td>
      <td>43</td>
      <td>29</td>
      <td>6</td>
      <td>5</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>5</td>
      <td>3</td>
      <td>13</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>34</td>
      <td>119</td>
      <td>66</td>
      <td>40</td>
      <td>41</td>
      <td>28</td>
      <td>18</td>
      <td>4</td>
      <td>4</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>14</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>43</td>
      <td>128</td>
      <td>74</td>
      <td>32</td>
      <td>32</td>
      <td>30</td>
      <td>20</td>
      <td>12</td>
      <td>6</td>
      <td>3</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>4</td>
      <td>13</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>37</td>
      <td>116</td>
      <td>62</td>
      <td>36</td>
      <td>36</td>
      <td>27</td>
      <td>11</td>
      <td>8</td>
      <td>4</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>27</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>39</td>
      <td>102</td>
      <td>60</td>
      <td>43</td>
      <td>40</td>
      <td>19</td>
      <td>19</td>
      <td>8</td>
      <td>5</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>5</td>
      <td>21</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>50</td>
      <td>107</td>
      <td>56</td>
      <td>26</td>
      <td>22</td>
      <td>15</td>
      <td>8</td>
      <td>5</td>
      <td>2</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>27</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>41</td>
      <td>99</td>
      <td>36</td>
      <td>32</td>
      <td>21</td>
      <td>7</td>
      <td>14</td>
      <td>6</td>
      <td>3</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>5</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>35</td>
      <td>80</td>
      <td>38</td>
      <td>27</td>
      <td>18</td>
      <td>9</td>
      <td>7</td>
      <td>3</td>
      <td>0</td>
      <td>5</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>10</td>
      <td>45</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>38</td>
      <td>77</td>
      <td>44</td>
      <td>15</td>
      <td>13</td>
      <td>11</td>
      <td>2</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>6</td>
      <td>27</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>19</td>
      <td>64</td>
      <td>24</td>
      <td>17</td>
      <td>15</td>
      <td>3</td>
      <td>3</td>
      <td>4</td>
      <td>3</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>40</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>12</td>
      <td>51</td>
      <td>24</td>
      <td>17</td>
      <td>15</td>
      <td>9</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>5</td>
      <td>64</td>
    </tr>
    <tr>
      <th>2016</th>
      <td>16</td>
      <td>44</td>
      <td>20</td>
      <td>16</td>
      <td>12</td>
      <td>7</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>9</td>
      <td>53</td>
    </tr>
    <tr>
      <th>2017</th>
      <td>18</td>
      <td>39</td>
      <td>17</td>
      <td>10</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>6</td>
      <td>11</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2018</th>
      <td>9</td>
      <td>30</td>
      <td>15</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>5</td>
      <td>6</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2019</th>
      <td>13</td>
      <td>24</td>
      <td>10</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>9</td>
      <td>75</td>
    </tr>
    <tr>
      <th>2020</th>
      <td>8</td>
      <td>33</td>
      <td>9</td>
      <td>5</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>9</td>
      <td>56</td>
    </tr>
    <tr>
      <th>2021</th>
      <td>8</td>
      <td>27</td>
      <td>6</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>3</td>
      <td>7</td>
      <td>59</td>
    </tr>
    <tr>
      <th>2022</th>
      <td>4</td>
      <td>27</td>
      <td>8</td>
      <td>5</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>6</td>
      <td>12</td>
      <td>95</td>
    </tr>
  </tbody>
</table>
<p>40 rows × 100 columns</p>
</div>



Basic statistics:
1.  Proportion Equal-Age-Group Marriages.
2.  Proportion of Marriages by Bride-Groom Age Differential.
3.  Proportion of Groom age groups by Bride age groups.
4.  Proportion of Bride age groups by Groom age groups.


```python
df_a_p = df_a.div(df_a.sum(axis=1), axis=0).mul(100).copy(deep=True)
plt.plot(df_a_p)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_25_0.svg)
    



```python
df_a_p_simp = pd.DataFrame.from_dict(
    dict(
        **{
            f'Bride {i*5} Years Older': df_a_p.loc[:,df_a_p.columns.get_level_values('Brides').codes-df_a_p.columns.get_level_values('Grooms').codes==i].sum(axis=1) for i in range(4, 0, -1)
        }, 
        **{'Equal Age Groups': df_a_p.loc[:,df_a_p.columns.get_level_values('Brides')==df_a_p.columns.get_level_values('Grooms')].sum(axis=1)}, 
        **{
            f'Bride {i*5} Years Younger': df_a_p.loc[:,df_a_p.columns.get_level_values('Brides').codes-df_a_p.columns.get_level_values('Grooms').codes==-i].sum(axis=1) for i in range(1, 5, 1)
        }, 
    ), 
    orient='columns'
)
plt.figure(figsize=(9, 6))
plt.plot(df_a_p_simp)
plt.legend(df_a_p_simp.columns)
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_26_0.svg)
    



```python
df_a_p_b = df_a.stack(level=['Grooms'], future_stack=True).copy(deep=True)
if not isinstance(df_a_p_b, pd.DataFrame):
    df_a_p_b = df_a_p_b.to_frame()
df_a_p_b = df_a_p_b.div(df_a_p_b.groupby(by=['Year']).sum()).mul(100)
_, axs = plt.subplots(3, 3, figsize=(15, 12), sharey=True, sharex=True)
for ax, i in zip(axs.flat, range(9)):
    sns.lineplot(data=df_a_p_b, x='Year', y=df_a_p_b.columns[i], hue='Grooms', ax=ax)
    ax.legend(title='Groom', loc=8, bbox_to_anchor=(0.5, 1), ncols=5, fontsize='x-small')
    ax.set_ylabel('Percent')
    ax.set_title(f'Bride: {df_a_p_b.columns[i]}', pad=48)
plt.tight_layout()
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_27_0.svg)
    



```python
df_a_p_g = df_a.stack(level=['Brides'], future_stack=True).copy(deep=True)
if not isinstance(df_a_p_g, pd.DataFrame):
    df_a_p_g = df_a_p_g.to_frame()
df_a_p_g = df_a_p_g.div(df_a_p_g.groupby(by=['Year']).sum()).mul(100)
_, axs = plt.subplots(3, 3, figsize=(15, 12), sharey=True, sharex=True)
for ax, i in zip(axs.flat, range(9)):
    sns.lineplot(data=df_a_p_g, x='Year', y=df_a_p_g.columns[i], hue='Brides', ax=ax)
    ax.legend(title='Bride', loc=8, bbox_to_anchor=(0.5, 1), ncols=5, fontsize='x-small')
    ax.set_ylabel('Percent')
    ax.set_title(f'Groom: {df_a_p_g.columns[i]}', pad=48)
plt.tight_layout()
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```


    
![svg](/blog/marriage-patterns/output_28_0.svg)
    


The story is straightforward: Grooms are typically older than brides, but otherwise brides and grooms generally try to marry within their age range.

This looks like a story about culture and tradition.
Traditionally, arguably there is stigma around males dating and marrying women much older than them (unless they are still very young),
whereas for women there is pressure to marry as young as possible due to cultural pressure to have children (which is biologically time-gated).
Finally, there is also strong stigma against dating and marrying very far out of one's age group (e.g., creeps and cougars/sugar daddies and mommies)

Perhaps as time goes by and culture changes and biological limits are overcome by technology, we might see more matches where the brides are older than grooms.
However, the stigma against extreme age disparities are likely here to stay for good reason (power imbalance between a much older/richer/more mature person vs a younger person), regardless of the gender of either side of the disparity.

##  2.  Marriage Success (Matching) Rates

These questions concern how successful are singles in transitioning to matches in the marriage market.
This is a different set of questions from those about the patterns of realised matches.
This is because the distribution of actual matches rarely reflects the distribution of the actual population that matches draw from, due to differential success (matching) rates.

First, we need to actually find population distribution data of education qualifications and age groups, by gender.


```python
datasets.search([r'(?i:\bmarital)', r'(?i:\bage(?![dD]))', r'(?i:\bsex)'])
```

    {
      "d_e2475676af29ec78749f1b22cf8b301c": "Residents Outside the Labour Force Aged 15 Years and Over by Marital Status, Age and Sex",
      "d_3a5b19d550c8542ac0d36851ad5c1099": "Resident Households by Age Group, Marital Status and Sex of Head of Household",
      "d_e19478b30d8f5cd6a1dc482bf2e46eb7": "Resident Labour Force Aged 15 Years and Over by Marital Status, Age and Sex",
      "d_a8140be10edc76f440b6a4a9745db1bd": "Resident Population Aged 15 Years and Over by Age Group, Marital Status, Sex and Residential Status",
      "d_f191bd4c393c21d0eb88ee96e614945f": "Resident Population Aged 15 Years and Over by Age Group, Marital Status, Sex and Ethnic Group",
      "d_87d2c457c7b93cfa84372b483f75553b": "Resident Population Aged 15 Years and Over by Age Group, Marital Status, Sex and Highest Qualification Attained"
    }



```python
df_age_olf = datasets.retrieve_dataset('d_e2475676af29ec78749f1b22cf8b301c')
df_age_olf = df_age_olf.drop(columns=['_id'])
df_age_lf = datasets.retrieve_dataset('d_e19478b30d8f5cd6a1dc482bf2e46eb7')
df_age_lf = df_age_lf.drop(columns=['_id'])
df_age = df_age_olf.merge(right=df_age_lf, on=['year', 'sex', 'marital_status', 'age'], how='outer')
df_age['population'] = df_age['outside_labour_force'] + df_age['labour_force']
df_age['sex'] = df_age['sex'].replace({'male': 'Male', 'female': 'Female'})
df_age['marital_status'] = df_age['marital_status'].replace({'married': 'Married', 'single': 'Single', 'widowed_divorced': 'Separated'})
df_age['age'] = df_age['age'].replace({'70_and_over': '70+'})
df_age = df_age.rename(columns={'year': 'Year', 'sex': 'Sex', 'marital_status': 'Marital', 'age': 'Age', 'population': 'Population'})
df_age['Sex'] = pd.Categorical(df_age['Sex'], ['Male', 'Female'], ordered=False)
df_age['Marital'] = pd.Categorical(df_age['Marital'], ['Married', 'Single', 'Separated'], ordered=False)
df_age['Age'] = pd.Categorical(df_age['Age'], ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70+'], ordered=True)
df_age = df_age.set_index(keys=['Year', 'Sex', 'Marital', 'Age'])['Population']
df_age = df_age.unstack(level=['Marital'])
df_age['NonMarried'] = df_age['Single'] + df_age['Separated']
df_age = df_age[['Married', 'NonMarried']]
df_age
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Marital</th>
      <th>Married</th>
      <th>NonMarried</th>
    </tr>
    <tr>
      <th>Year</th>
      <th>Sex</th>
      <th>Age</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">1991</th>
      <th rowspan="5" valign="top">Male</th>
      <th>15-19</th>
      <td>300</td>
      <td>122700</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>5300</td>
      <td>115600</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>45700</td>
      <td>93100</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>96400</td>
      <td>48700</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>108800</td>
      <td>23400</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">2023</th>
      <th rowspan="5" valign="top">Female</th>
      <th>50-54</th>
      <td>127300</td>
      <td>39600</td>
    </tr>
    <tr>
      <th>55-59</th>
      <td>119500</td>
      <td>41500</td>
    </tr>
    <tr>
      <th>60-64</th>
      <td>111100</td>
      <td>39300</td>
    </tr>
    <tr>
      <th>65-69</th>
      <td>91600</td>
      <td>40400</td>
    </tr>
    <tr>
      <th>70+</th>
      <td>126800</td>
      <td>123400</td>
    </tr>
  </tbody>
</table>
<p>720 rows × 2 columns</p>
</div>



A basic statistic to ask is about the marriage rate by age group and gender.
This is because if one uses the entire pool of non-married people as the candidate pool to draw matches from,
then increases and decreases in the marriage rate of a group is informative about the matching success rate of that group, even before comparing the non-married population to realised matches.


```python
df_age_m = df_age.xs(('Male',), 0, ('Sex',)).copy(deep=True)
df_age_m = df_age_m.apply(lambda row: 100 * row['Married'] / row.sum(), axis=1).rename('Rate').to_frame()
df_age_f = df_age.xs(('Female',), 0, ('Sex',)).copy(deep=True)
df_age_f = df_age_f.apply(lambda row: 100 * row['Married'] / row.sum(), axis=1).rename('Rate').to_frame()
_, axs = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
sns.lineplot(df_age_m, x='Age', y='Rate', hue='Year', palette='viridis_r', ax=axs[0])
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45)
axs[0].set_title('Male')
sns.lineplot(df_age_f, x='Age', y='Rate', hue='Year', palette='viridis_r', ax=axs[1])
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45)
axs[1].set_title('Female')
plt.suptitle('Marriage Rate, by Age-Group, Year')
plt.tight_layout()
plt.show()
plt.gcf().clear()
plt.close(plt.gcf())
```

    /tmp/ipykernel_15530/282482770.py:7: UserWarning: set_ticklabels() should only be used with a fixed number of ticks, i.e. after set_ticks() or using a FixedLocator.
      axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45)
    /tmp/ipykernel_15530/282482770.py:10: UserWarning: set_ticklabels() should only be used with a fixed number of ticks, i.e. after set_ticks() or using a FixedLocator.
      axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45)



    
![svg](/blog/marriage-patterns/output_35_1.svg)
    


Another basic statistic to ask is about the tightness of the marriage market.
This is because knowing the relative amount of choices that either side of a matching market has is informative about the kinds and quality of matches that result.


```python
df_age_r = df_age['NonMarried'].unstack(level='Sex').apply(lambda row: row['Male'] / row['Female'], axis=1).rename('Ratio').to_frame()
sns.lineplot(df_age_r, x='Age', y='Ratio', hue='Year', palette='viridis_r')
plt.title('Male-Female Tightness Ratio, by Age-Group, Year')
plt.xticks(rotation=45)
plt.show()
```


    
![svg](/blog/marriage-patterns/output_37_0.svg)
    


Another way to display this information is by birth cohort.


```python
df_bc = df_age['NonMarried'].unstack(level='Sex').copy(deep=True)
df_bc['Cohort'] = df_bc.index.get_level_values('Year') - (df_bc.index.get_level_values('Age').codes + 3) * 5
df_bc = df_bc.set_index(keys=['Cohort'], append=True)
df_bc = df_bc.droplevel(level=['Year'], axis=0)
df_bc = df_bc.swaplevel(i=0, j=1, axis=0)
df_bc = df_bc.sort_index(axis=0)
df_bc_r = df_bc.apply(lambda row: row['Male'] / row['Female'], axis=1).rename('Ratio').to_frame()
sns.lineplot(df_bc_r, x='Age', y='Ratio', hue='Cohort', palette='viridis_r')
plt.title('Male-Female Tightness Ratio, by Age-Group, Birth Cohort')
plt.xticks(rotation=45)
plt.show()
```


    
![svg](/blog/marriage-patterns/output_39_0.svg)
    


All representations are consistent with the same story:
Over the years, the tightness curve has flattened, driven mechanically by a fall in the marriage rates of women.

Previously, men married later than women and married women younger than them.
This is seen in the high rates of marriage of women and the earlier peak in marriage rates compared to men.
More recently, men married more within their age groups/birth cohorts,
leading to more older non-married men and less younger non-married men.
Mechanically, the low marriage rates of men in earlier years would likely be due to competition with older men who may have been more attractive due to higher socioeconomic status and stability.

Another striking fact is that cohort subcurves seem to occupy quite distinct levels on the overall tightness ratio curve, indicating that much of the observed shift in the tightness ratio curve is being driven by differential marriage patterns between cohorts, with younger cohorts flattening out at a relatively rapid pace.

Unclear what caused these shifts toward a more egalitarian marriage market, but changes in culture and tradition would be a plausible hypothesis especially given the distinctiveness of cohort-wise tightness ratio curves.


```python
datasets.search([r'(?i:\bmarital|\bsingle|\bmarried|\bannual)', r'(?i:\bsex|\bgender)', r'(?i:\bqual|\beduc)'])
```

    {
      "d_87d2c457c7b93cfa84372b483f75553b": "Resident Population Aged 15 Years and Over by Age Group, Marital Status, Sex and Highest Qualification Attained",
      "d_4c689993c2f4b165f420d29cbb0c8b51": "Resident Population Aged 15 Years and Over by Highest Qualification Attained, Marital Status, Sex and Ethnic Group",
      "d_504d991189c4cd84689f7da9abc63a5a": "Singapore Residents Aged 25 Years & Over By Highest Qualification Attained, Sex And Age Group, Annual",
      "d_5c4667aee18cb4b99528b9d98effb579": "Proportion Of Singles Among Resident Population By Selected Age Group, Sex And Highest Qualification Attained, Annual"
    }


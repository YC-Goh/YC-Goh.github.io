
#%%

import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import seaborn as sns

#%%

def display_all_columns(data:pd.DataFrame)->None:
    with pd.option_context('display.max_columns', None):
        display(data)

#%%

def display_all_rows(data:pd.DataFrame)->None:
    with pd.option_context('display.max_rows', None):
        display(data)

#%%

def display_full_table(data:pd.DataFrame)->None:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(data)

#%%

def plot_singlecol_data(data:pd.DataFrame, ylabel:str, splitplot:bool=True)->tuple[plt.Figure,axes.Axes]:
    y_levels = data.columns.unique()
    if splitplot:
        n_y = y_levels.nunique()
    else:
        n_y = 1
    h = 1 * 3
    w = n_y * (3 * (3 / 2))
    fig, axs = plt.subplots(1, n_y, figsize=(w, h), sharex=True, sharey=True)
    if splitplot:
        axs[0].set_ylabel(ylabel)
    else:
        axs:axes.Axes
        axs.set_ylabel(ylabel)
    if splitplot:
        for y in y_levels:
            i_y = y_levels.get_indexer_for([y])[0]
            ax_y:axes.Axes = axs[i_y]
            ax_y.set_facecolor(('white', 0.5))
            ax_y.set_title(y)
            try:
                sns.lineplot(data.loc[:,y], ax=ax_y, c=sns.color_palette('Dark2')[0])
            except:
                pass
    else:
        axs.set_facecolor(('white', 0.5))
        try:
            sns.lineplot(data, ax=axs, dashes=False, palette='Dark2', markers=True)
            h, l = axs.get_legend_handles_labels()
            t = axs.get_legend().get_title().get_text()
            axs.legend(h, l, fontsize='xx-small', title=t, title_fontsize='xx-small')
        except:
            pass
    fig.get_tight_layout()
    fig.set_facecolor(('white', 0.5))
    return fig, axs

#%%

def plot_multicol_data(data:pd.DataFrame, x_level:str, y_level:str)->tuple[plt.Figure,axes.Axes]:
    x_levels = data.columns.unique(x_level)
    y_levels = data.columns.unique(y_level)
    n_x = x_levels.nunique()
    n_y = y_levels.nunique()
    if n_y == 1:
        h = n_y * 3
        w = n_x * (3 * (3 / 2))
        fig, axs = plt.subplots(n_y, n_x, figsize=(w, h), sharex=True, sharey=True)
    else:
        h = n_x * 3
        w = n_y * (3 * (3 / 2))
        fig, axs = plt.subplots(n_x, n_y, figsize=(w, h), sharex=True, sharey=True)
    for x in x_levels:
        i_x = x_levels.get_indexer_for([x])[0]
        if n_y > 1:
            axs[i_x][0].set_ylabel(f'{x_level.title()}: {x}')
        else:
            axs[i_x].set_title(f'{x_level.title()}: {x}')
        for y in y_levels:
            i_y = y_levels.get_indexer_for([y])[0]
            if n_y > 1:
                ax_xy:axes.Axes = axs[i_x][i_y]
            else:
                ax_xy:axes.Axes = axs[i_x]
            ax_xy.set_facecolor(('white', 0.5))
            if i_x == 0:
                if n_y > 1:
                    ax_xy.set_title(f'{y_level.title()}: {y}')
                else:
                    ax_xy.set_ylabel(f'{y_level.title()}: {y}')
            if n_y == 1 or i_x == n_x - 1:
                ax_xy.tick_params(axis='x', labelrotation=45)
            try:
                plot_data = data.xs((x,y,), 1, (x_level,y_level,)).copy(deep=True)
                if plot_data.columns.nlevels == 1:
                    if plot_data.columns.size == 1:
                        plot_data = plot_data.iloc[:,[0]]
                    sns.lineplot(plot_data, ax=ax_xy, dashes=False, palette='Dark2', markers=True)
                    h, l = ax_xy.get_legend_handles_labels()
                    t = ax_xy.get_legend().get_title().get_text()
                    ax_xy.legend(h, l, fontsize='xx-small', title=t, title_fontsize='xx-small')
                else:
                    plot_data = plot_data.iloc[:,0]
                    sns.lineplot(plot_data, ax=ax_xy, c=sns.color_palette('Dark2')[0])
            except:
                pass
    fig.get_tight_layout()
    fig.set_facecolor(('white', 0.5))
    return fig, axs

#%%

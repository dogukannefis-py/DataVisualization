#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def line_plot(df, col):
    
    x = df.index.tolist()
    y = df[col].tolist()
    
    trace = {'type':  'scatter', 
             'x'   :  x,
             'y'   :  y,
             'mode' : 'markers',
             'marker': {'colorscale':'reds', 'opacity': 0.5}
            }
    data   = Data([trace])
    layout = {'title': 'Line plot of {}'.format(col), 'titlefont': {'size': 30},
              'xaxis' : {'title' :'Data Index', 'titlefont': {'size' : 20}},
              'yaxis' : {'title': col, 'titlefont' : {'size': 20}},
              'hovermode': 'closest'
             }
    fig = Figure(data = data, layout = layout)
    return fig


# In[ ]:


def bar_plot(df, data_pt):
    
    """
        Bar Plot with sorted features
    """
    
    x=df.loc[data_pt]
    y= df.columns.tolist()
    sorte=x.tolist()
    a=sorted(zip(sorte, y))[-10:]
    y=[y for _, y in a]
    ## soru burda yapıp altı ona göre duzeliyecegim birde
    
    x = df[y].loc[data_pt]
    
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    #title={'text': "<b>Comparing features with Golden  for Cycle {}".format(cycle),
     #      'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}

    
    trace = {'type': 'bar',
             'orientation':'h',
             'x'   : x,
             'y'   : y}
    data = Data([trace])
    layout = {'title' : "<b>Reconstruction error in each dimension for cycle{}".format(data_pt),
              'titlefont':{'size' : 20},
              'xaxis' : {'title': '<b>Reconstruction Error',
                         'titlefont':{'size' : 20},
                         'tickangle': -45, 'tickfont': {'size':15} ,},
    
              'yaxis' : {'title': '<b>Features',
                         'titlefont':{'size' : 20},
                         'tickfont': {'size':15},},
              'margin' : {'l':100, 'r' : 1, 'b': 200, 't': 100, 'pad' : 1},
              'height' : 600, 'width' : 800,
             }
    
    fig = Figure(data = data, layout = layout)
    
    return pyo.iplot(fig)


# In[ ]:


def Radar_Map(dataframe,outlier):
    
    x = dataframe.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    x_scaled = min_max_scaler.fit_transform(x)
    df_normalized = pd.DataFrame(x_scaled,columns=dataframe.columns,index=dataframe.index)
    
    ##returns golden cycle with confidence interval for each feature
    golden,upper,lower=golden_cycle_creator(df_normalized,650,1206) 
    
    g_values=golden[golden.columns].iloc[0]
    upper_values=upper[upper.columns].iloc[0]
    lower_values=lower[lower.columns].iloc[0]
    
    outlier_values = df_normalized[df_normalized.columns].loc[outlier] 
    labels=dataframe.columns.to_list()

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=outlier_values,
          theta=labels,
          fill='toself',
          name='Cycle'
    ))
    fig.add_trace(go.Scatterpolar(
          r=g_values,
          theta=labels,
          fill='toself',
          name='Golden'
    ))
     
    fig.add_trace(go.Scatterpolar(
          r=upper_values,
          theta=labels,
          name='Upper Bound'
    ))
    
    fig.add_trace(go.Scatterpolar(
          r=lower_values,
          theta=labels,
          name='Lower Bound'
    ))

    fig.update_layout(height=1000, width=1300)

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1]
        )),
      showlegend=True
    )

    fig.show()


# In[ ]:





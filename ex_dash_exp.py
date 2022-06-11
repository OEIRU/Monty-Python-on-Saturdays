import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import approximate_taylor_polynomial

app = dash.Dash(__name__)

t = np.linspace(-1, 6, 100)
fun = lambda x: np.exp(x)*np.sin(x)
fun_str = 'e^x*sin(x)'
y0 = fun(t)
degree = 3
x0 = 0


def tailor_to_str(taylor, x_0) -> str:
    """
    строковое представление
    :param taylor: разложение в ряд Тейлора
    :param x_0: точка аппроксимации
    :return: строка вида a_n(x-x0)^n-1+...a_0
    """
    sf = lambda x: "{:e}".format(x)
    elems = [f'{sf(a)}(x-{x_0})^{taylor.order - i}' if taylor.order - i > 1
             else f'{sf(a)}(x-{x_0})' if taylor.order - i == 1 else f'{sf(a)}'
             if x_0 else f'{sf(a)}x^{taylor.order - i}' if taylor.order - i > 1
             else f'{sf(a)}x' if taylor.order - i == 1 else f'{sf(a)}'
             for i, a in enumerate(taylor.coeffs)]
    return ('+'.join(elems)).replace('--', '+').replace('+-', '-')


def plot_func_and_taylor(v_degree, v_x0, v_fun):
    """График исходной функции и ее разложения в ряд Тейлора
    :param v_fun: функция
    :param v_degree: степень полинома
    :param v_x0: точка аппроксимации
    """
    nfig = go.Figure()
    nfig.add_trace(go.Scatter(x=t, y=y0, mode='lines', name=f'{fun_str}'))
    y_taylor = approximate_taylor_polynomial(v_fun, v_x0, v_degree, 1)
    nfig.add_trace(go.Scatter(x=t, y=y_taylor(t - v_x0), mode='lines', name=f'{tailor_to_str(y_taylor, v_x0)}'))
    nfig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return nfig


# структура страницы
app.layout = html.Div(children=[
    html.H1(children='Пример разложения в ряд Тейлора экспоненты'),

    html.Div(children=[
        html.P("Степень полинома"),
        dcc.Slider(id='members', min=1, max=12, step=1, value=degree,
                   marks={x: str(x) for x in range(1, 13)}),
        html.P("Точка аппроксимации"),
        dcc.Slider(id='point', min=-0.5, max=2.5, step=0.5, value=x0,
                   tooltip={"placement": "bottom", "always_visible": True}),
        dcc.Graph(
            id='example-graph',
            figure=plot_func_and_taylor(degree, x0, fun)
        )

    ]),
])


# обработка изменения параметров
@app.callback(
    Output("example-graph", "figure"),
    [Input("members", "value"), Input("point", "value")])
def update_line_members(v_degree, v_x0):
    return plot_func_and_taylor(v_degree, v_x0, fun)


if __name__ == '__main__':
    app.run_server(debug=True)

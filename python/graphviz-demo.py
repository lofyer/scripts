from graphviz import Digraph
dot = Digraph(comment='这是一个有向图')

dot.node('A', '医生', shape="box", image="asd.jpeg")
dot.node('B', '医生')
dot.node('C', '护士')

dot.edges(['AB', 'AC'])
dot.edge('B', 'C')

dot.format = 'png'
dot.render('output-graph.gv', view=True)

from IPython.display import display, Image
Image(dot.render('output-graph.png', format="png"))

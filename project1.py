import math
import matplotlib.pyplot as pt
import numpy
import random
import time

class node:
    def __init__(self, value):
        self.value = value 
        self.children = []

class tree:
    def __init__(self):
        self.fitness = 1
        self.nodes=[]
    def Add_newChild(self, node, parent):
        self.nodes.append(node)
        parent.children.append(node)
    def Init_Root(self, root):
        self.nodes.append(root) 


All_operators = ['-', '+','/','*']

def Build_Tree(tr, parent, node_count, count):
    if count == node_count:
        tr.Add_newChild(node('x'), parent)
        tr.Add_newChild(node('x'), parent)
        return
    node1 = node(random.choice(All_operators))
    tr.Add_newChild(node1, parent)
    node2 = node(random.choice(All_operators))
    tr.Add_newChild(node2, parent)
    Build_Tree(tr, node1, node_count, count+1)
    Build_Tree(tr, node2, node_count, count+1)

#harchi fitness kamter, behtar
def Calc_fitness(y_funcs, tree_Eval):
    Sum = 0
    for i in range(len(y_funcs)):
        Sum += ( (y_funcs[i] - tree_Eval[i]) * (y_funcs[i] - tree_Eval[i]) )
    enheraf_meyar = Sum/(len(y_funcs))
    return enheraf_meyar

#peida kardane behtarin derakht, ba kamtrin fitness
def Find_bestTree(population):
    best_tree = population[0]
    n = len(population)
    for i in range(n):
        if population[i].fitness < best_tree.fitness:
            best_tree = population[i]
    return best_tree

def Calculate_Tree(tree, x, pos=0):
    if(tree.nodes[pos].value == 'x'):
        return x , pos
    if(tree.nodes[pos].value in All_operators):
        Operatorpos = pos
        left , pos = Calculate_Tree(tree,x,pos+1)    
        right , pos = Calculate_Tree(tree,x,pos+1) 
        if(tree.nodes[Operatorpos].value == '-'):
            return left - right, pos
        elif(tree.nodes[Operatorpos].value == '+'):
            return left + right, pos
        elif(tree.nodes[Operatorpos].value == '/'):
            if right != 0:
                return left / right, pos
            else:
                right = 0.0001  
                return left / right, pos
        elif(tree.nodes[Operatorpos].value == '*'):
            return left * right, pos  

fitCount = 0
def make_Child(mother,father):
    child = ['x','x']
    m_Operatorscount = (len(mother.nodes)-1)//2
    f_Operatorscount = (len(father.nodes)-1)//2
    # num_radif = int(math.log((len(child)+1),2))
    # while num_radif != int(num_radif):
    while math.log((len(child)+1),2) != int(math.log((len(child)+1),2)):
        child = []
        mother_first = numpy.random.randint(0,m_Operatorscount)
        father_first = numpy.random.randint(0,f_Operatorscount)
        mother_last = numpy.random.randint(mother_first,m_Operatorscount)
        father_last = numpy.random.randint(father_first,f_Operatorscount)
        # child = father.nodes[:father_first] + mother.nodes[mother_first : mother_last] + father.nodes[father_last :f_Operatorscount] + mother.nodes[mother_last :m_Operatorscount]
        child = mother.nodes[:mother_first] + father.nodes[father_first : father_last] + mother.nodes[mother_last :m_Operatorscount]
        global fitCount
        fitCount += 1

    for i in range ((len(child)+1)):
        n_ch = node('x')
        child.append(n_ch)
    return child



def select_LocalBest(trees,size):  
    random_pop = []
    random_pop = random.sample(trees, size)
    bestTree = random_pop[0]
    for i in range(size):
        if random_pop[i].fitness < bestTree.fitness:
            bestTree = random_pop[i]
    return bestTree


def test_Func (x):
    y = x*x
    return y

x_func = []
y_func = []
for i in numpy.arange(0, 20, 0.01):
    x_func.append(i)

for x in x_func:
    y_func.append(test_Func(x))

nasl = 0
startTime = time.time()

# jamiat avalie -- tedadi derakht amaliate random
All_trees = []
for i in range(400):
    tr = tree()
    # level_count = random.randint(1,2)
    level_count = 1
    # print(level_count)
    rand_op = random.choice(All_operators)
    root = node(rand_op)
    tr.Init_Root(root)
    node_count = (2**level_count)-1
    Build_Tree(tr,root,node_count,0)
    All_trees.append(tr)
nasl += 1

calcstree = []
for tr in All_trees:
    calcstree = []
    for x in x_func:
        calcstree.append(Calculate_Tree(tr, x, 0)[0])
    fitCount += 1
    tr.fitness = Calc_fitness(y_func, calcstree)


newPop = []
size = len(All_trees)//2
for i in range(2000):
    motherTree = select_LocalBest(All_trees, size)
    fatherTree = select_LocalBest(All_trees, size)
    child = make_Child(motherTree, fatherTree)
    childTree = tree()
    childTree.nodes = child
    calcAmounts = []
    for x in x_func:
        d = Calculate_Tree(childTree, x,0)[0]
        calcAmounts.append(d)
    child_fit = Calc_fitness(y_func, calcAmounts)
    fitCount += 1
    childTree.fitness = child_fit
    newPop.append(childTree)
nasl += 1

endtTime = time.time()
bestTree = Find_bestTree(newPop)
print("tabe takhmin zade shode(function tree):  ")
for B_node in bestTree.nodes:
    print(B_node.value)
print("shayestegi behtarin drakht(fitness):  " + str(bestTree.fitness))
print("zamane ejra(Total time):  " + str(endtTime - startTime))
print("nasl:  " + str(nasl))
print("tedad mohasebe shayestegi:  " + str(fitCount))


pt.plot(x_func, y_func, color='g', dashes = [18,1])
pt.xlabel('x')
pt.ylabel('y')
pt.title('original function diagram(green) & approximated diagram(red)')
pt.plot(x_func, calcAmounts, color='r', dashes = [6,3])
pt.show()
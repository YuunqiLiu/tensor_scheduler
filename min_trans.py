

from pyomo.environ import *


def get_min_trans(X0=1000,Y0=100,C=100,P=512,B=1000,detail=False):
    TOTAL_BUFFER_SIZE = B

    model = ConcreteModel()
    model.sx            = Var(within=NonNegativeIntegers)
    model.sy            = Var(within=NonNegativeIntegers)
    model.x             = Var(within=NonNegativeIntegers,bounds=(1,P))
    model.y             = Var(within=NonNegativeIntegers,bounds=(1,P))
    model.data_y        = Var()
    model.data_x        = Var()
    model.data_y_normal = Var()
    model.data_x_normal = Var()
    model.x_exp         = Var(within=NonNegativeIntegers,bounds=(2,5))
    model.y_exp         = Var(within=NonNegativeIntegers,bounds=(2,5))
    model.x_rate_int    = Var(within=NonNegativeIntegers)
    model.y_rate_int    = Var(within=NonNegativeIntegers)
    model.min_data_read = Var()


    model.conx_x_exp            = Constraint(expr = model.x == 2** model.x_exp)
    model.conx_y_exp            = Constraint(expr = model.y == 2** model.y_exp)

    model.cons_x_rate_int       = Constraint(expr= model.x_rate_int >= X0/model.x)
    model.cons_y_rate_int       = Constraint(expr= model.y_rate_int >= Y0/model.y)

    model.cons_x_rate_int2      = Constraint(expr= model.x_rate_int <= X0/model.x +1)
    model.cons_y_rate_int2      = Constraint(expr= model.y_rate_int <= Y0/model.y +1)

    # Input Buffer
    model.cons_sx_sy            = Constraint(expr= model.sx + model.sy <= TOTAL_BUFFER_SIZE)

    # PSUM Buffer
    model.cons_psum             = Constraint(expr= (model.x * model.y <= P))

    # DataY
    model.cons_datay            = Constraint(expr= (model.data_y_normal == model.x_rate_int*(Y0*C-model.sy)+model.sy))
    model.cons_detay2           = Constraint(expr= (model.data_y >= model.data_y_normal))
    model.cons_detay3           = Constraint(expr= (model.data_y >= Y0*C))

    # DataX
    model.cons_datax            = Constraint(expr= (model.data_x_normal == (model.y_rate_int*(model.x*C-model.sx)+model.sx)*model.x_rate_int))
    model.cons_detax2           = Constraint(expr= (model.data_x >= model.data_x_normal))
    model.cons_detax3           = Constraint(expr= (model.data_x >= X0*C))

    model.cons_min_data         = Constraint(expr = model.min_data_read == model.data_x + model.data_y)


    model.obj = Objective(expr=model.min_data_read*10000-model.x*29-model.y, sense = minimize)
    opt = SolverFactory('scip')
    solution = opt.solve(model)

    if detail:
        print("Psum X: %s" %    value(model.x))
        print("Psum Y: %s" %    value(model.y))
        print("Size X: %s" %    value(model.sx))
        print("Size Y: %s" %    value(model.sy))
        print(value(model.data_x_normal))
        print(value(model.data_y_normal))
        print(value(model.data_x))
        print(value(model.data_y))
        print("Min Data Read: %s" % value(model.min_data_read))
    return value(model.min_data_read)

for b in range(200,11000,200):
    print(b,'    ', get_min_trans(B=b))


get_min_trans(B=9800,detail=True)
get_min_trans(B=10000,detail=True)
get_min_trans(B=10200,detail=True)
get_min_trans(B=11000,detail=True)
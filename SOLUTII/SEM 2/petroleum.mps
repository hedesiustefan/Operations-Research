OBJSENSE
 MAX
NAME          Petroleum_Blending
ROWS
 N  OBJ
 L  Availability_C1
 L  Availability_C2
 L  Availability_C3
 G  Min_production_Super
 G  Min_C1_Super
 G  Min_production_Premium
 G  Min_C1_Premium
 G  Min_production_Extra
 G  Min_C1_Extra
 L  Max_C2_Super
 L  Max_C3_Premium
 G  Min_C2_Extra
COLUMNS
    x_C1_Super  Availability_C1   1.000000000000e0
    x_C1_Super  Min_production_Super   1.000000000000e0
    x_C1_Super  Min_C1_Super   5.000000000000e-1
    x_C1_Super  Max_C2_Super  -3.000000000000e-1
    x_C1_Super  OBJ        1.100000000000e1
    x_C1_Premium  Availability_C1   1.000000000000e0
    x_C1_Premium  Min_production_Premium   1.000000000000e0
    x_C1_Premium  Min_C1_Premium   6.000000000000e-1
    x_C1_Premium  Max_C3_Premium  -2.500000000000e-1
    x_C1_Premium  OBJ        8.000000000000e0
    x_C1_Extra  Availability_C1   1.000000000000e0
    x_C1_Extra  Min_production_Extra   1.000000000000e0
    x_C1_Extra  Min_C1_Extra   4.000000000000e-1
    x_C1_Extra  Min_C2_Extra  -1.000000000000e-1
    x_C1_Extra  OBJ        6.000000000000e0
    x_C2_Super  Availability_C2   1.000000000000e0
    x_C2_Super  Min_production_Super   1.000000000000e0
    x_C2_Super  Min_C1_Super  -5.000000000000e-1
    x_C2_Super  Max_C2_Super   7.000000000000e-1
    x_C2_Super  OBJ        1.300000000000e1
    x_C2_Premium  Availability_C2   1.000000000000e0
    x_C2_Premium  Min_production_Premium   1.000000000000e0
    x_C2_Premium  Min_C1_Premium  -4.000000000000e-1
    x_C2_Premium  Max_C3_Premium  -2.500000000000e-1
    x_C2_Premium  OBJ        1.000000000000e1
    x_C2_Extra  Availability_C2   1.000000000000e0
    x_C2_Extra  Min_production_Extra   1.000000000000e0
    x_C2_Extra  Min_C1_Extra  -6.000000000000e-1
    x_C2_Extra  Min_C2_Extra   9.000000000000e-1
    x_C2_Extra  OBJ        8.000000000000e0
    x_C3_Super  Availability_C3   1.000000000000e0
    x_C3_Super  Min_production_Super   1.000000000000e0
    x_C3_Super  Min_C1_Super  -5.000000000000e-1
    x_C3_Super  Max_C2_Super  -3.000000000000e-1
    x_C3_Super  OBJ        9.000000000000e0
    x_C3_Premium  Availability_C3   1.000000000000e0
    x_C3_Premium  Min_production_Premium   1.000000000000e0
    x_C3_Premium  Min_C1_Premium  -4.000000000000e-1
    x_C3_Premium  Max_C3_Premium   7.500000000000e-1
    x_C3_Premium  OBJ        6.000000000000e0
    x_C3_Extra  Availability_C3   1.000000000000e0
    x_C3_Extra  Min_production_Extra   1.000000000000e0
    x_C3_Extra  Min_C1_Extra  -6.000000000000e-1
    x_C3_Extra  Min_C2_Extra  -1.000000000000e-1
    x_C3_Extra  OBJ        4.000000000000e0
RHS
    RHS       Availability_C1   4.500000000000e3
    RHS       Availability_C2   2.700000000000e3
    RHS       Availability_C3   3.500000000000e3
    RHS       Min_production_Super   3.000000000000e3
    RHS       Min_C1_Super   0.000000000000e0
    RHS       Min_production_Premium   3.000000000000e3
    RHS       Min_C1_Premium   0.000000000000e0
    RHS       Min_production_Extra   3.000000000000e3
    RHS       Min_C1_Extra   0.000000000000e0
    RHS       Max_C2_Super   0.000000000000e0
    RHS       Max_C3_Premium   0.000000000000e0
    RHS       Min_C2_Extra   0.000000000000e0
BOUNDS
ENDATA

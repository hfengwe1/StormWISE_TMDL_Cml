# StormWISE_GrnAcr model Cost minimization with multiple benefits as constraints 
# using the Philadelphia Water Department Greened Acre as decision variables
# In this model file, parameters s and u are calculated outside of AMPL, such
# as by the stormwise_grnacr.py program.

set I;	# community zones
set J; 	# land-use categories
set K;	# bmp/lid categories
set KONJ{J} within K; # bmp/lid categories that are deployed on each land-use 
set T;	# benefit categories
set Ta; # index of ancillary benefits
set Ts; # index of stormwater benefits
set Kg; # index of ground GI
set Kr; # index of roof GI
set weighting; # weightings elicited from three methods

###
param Bmin{T}; # default 0.0;		# lower bounds for benefits in standard units
###
param bud default 10000;		# default budget (10,000 k$)
param scale{T};					# scale factors for benefits - may include unit conversions and fractions
param area{I,J};					# area in zone i having land-use j
param s{I,J,K,T};
param u{I,J,K};
param f{I,J,K};
param w1{weighting,Ta};			# weights elicited from workshops
param w{t in Ta};
param area_g{i in I,j in J} =f[i,j, "3_tree_trench"]*area[i,j];			# maximum available gound area for GI
param area_r{i in I,j in J} =f[i,j, "8_cistern"]*area[i,j];				# maximum available roof area for GI
param 1_min{t in Ta};
param 2_range{t in Ta};
param cost{J,K};

var x{i in I,j in J,k in K} >=0, <= u[i,j,k];							# amout to invest - Decision Variables
var b_gi{t in T} = sum {i in I, j in J, k in K} s[i,j,k,t]*x[i,j,k]*scale[t];
var total_cost = sum{i in I,j in J, k in K} x[i,j,k];
var gi_area{k in K} = sum{i in I,j in J } x[i,j,k]/cost[j,k];

maximize A_benefits: sum {t in Ta} w[t]*(b_gi[t]-1_min[t])/2_range[t]; 

subject to benefits{t in T}: sum{i in I, j in J, k in K} s[i,j,k,t]*x[i,j,k] >= Bmin[t];
subject to budget: sum { i in I, j in J, k in K} x[i,j,k] <= bud;
subject to ground{i in I,j in J}: sum{k in Kg} x[i,j,k]/cost[j,k] <=area_g[i,j];
subject to roof{i in I,j in J}: sum{k in Kr}  x[i,j,k]/cost[j,k] <= area_r[i,j];

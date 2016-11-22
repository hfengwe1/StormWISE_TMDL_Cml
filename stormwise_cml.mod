# StormWISE_CML model Cost minimization with multiple benefits as constraints 
# In this model file, parameters s and u are calculated outside of AMPL, such
# as by the stormwise_tmdl.py program.

set I;	# drainage zones
set J; 	# land-use categories
set K;	# bmp/lid categories
set KONJ{J} within K; # bmp/lid categories that are deployed on each land-use 
set T;	# benefit categories
set Ta; # index of ancillary benefits
set Ts; # index of stormwater benefits
set Kg; # index of ground GI
set Kr; # index of roof GI
set weighting; # weightings elicited from three methods

#param Bmin{T}; # default 0.0;		# lower bounds for benefits in standard units
#param s{I,j in J,KONJ[j],T}; #benefit slopes
#param u{I,j in J,KONJ[j]};   # calculated upper spending limits
param bmin{T} default 0.0;		# lower bounds for benefits
param bud default 10000;            # default budget 10 million
param cost{j in J,k in K}; 	# marginal bmp/lid cost per unit of area treated 
param eta{K,T};	# reduction fraction or benefit multipliers
param scale{T};   	# scale factors for benefits - may include unit conversions or fraction of runoff
param export{j in J,t in T};	# export coefficient
param f{j in J,k in K};		# applicable area fraction
param area{J};	# area in zone i having land-use j
param s{j in J,k in K,t in T} = eta[k,t]*export[j,t]/cost[j,k];	# calculated benefit slopes
param u{j in J,k in K} = cost[j,k]*f[j,k]*area[j];				# calculated upper spending limits





var x{i in I,j in J,k in KONJ[j]} >= 0 <= u[i,j,k];	# amout to invest - Decision Variables

minimize investment: sum{i in I, j in J, k in KONJ[j]} x[i,j,k];

subject to benefits{t in T}: sum{i in I, j in J, k in KONJ[j]} s[i,j,k,t]*x[i,j,k] >= Bmin[t];

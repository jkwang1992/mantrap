Search.setIndex({docnames:["agents","controllers","environment","evaluation","filter","index","modules","solver","visualisation"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":2,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["agents.rst","controllers.rst","environment.rst","evaluation.rst","filter.rst","index.rst","modules.rst","solver.rst","visualisation.rst"],objects:{"mantrap.agents":{integrator_double:[0,0,0,"-"],integrator_single:[0,0,0,"-"]},"mantrap.agents.base":{discrete:[0,0,0,"-"],linear:[0,0,0,"-"]},"mantrap.agents.base.discrete":{DTAgent:[0,1,1,""]},"mantrap.agents.base.discrete.DTAgent":{check_feasibility_controls:[0,2,1,""],check_feasibility_trajectory:[0,2,1,""],control_limits:[0,2,1,""],detach:[0,2,1,""],dx_du:[0,2,1,""],dynamics:[0,2,1,""],dynamics_scalar:[0,2,1,""],expand_state_vector:[0,2,1,""],expand_trajectory:[0,2,1,""],go_to_point:[0,2,1,""],inverse_dynamics:[0,2,1,""],make_controls_feasible:[0,2,1,""],make_controls_feasible_scalar:[0,2,1,""],reachability_boundary:[0,2,1,""],reset:[0,2,1,""],roll_trajectory:[0,2,1,""],sanity_check:[0,2,1,""],unroll_trajectory:[0,2,1,""],update:[0,2,1,""]},"mantrap.agents.base.linear":{LinearDTAgent:[0,1,1,""]},"mantrap.agents.base.linear.LinearDTAgent":{dx_du:[0,2,1,""],reachability_boundary:[0,2,1,""],roll_trajectory:[0,2,1,""],unroll_trajectory:[0,2,1,""]},"mantrap.agents.integrator_double":{DoubleIntegratorDTAgent:[0,1,1,""]},"mantrap.agents.integrator_double.DoubleIntegratorDTAgent":{control_limits:[0,2,1,""],dynamics_scalar:[0,2,1,""],go_to_point:[0,2,1,""]},"mantrap.agents.integrator_single":{IntegratorDTAgent:[0,1,1,""]},"mantrap.agents.integrator_single.IntegratorDTAgent":{acceleration_max:[0,2,1,""],control_limits:[0,2,1,""],dynamics_scalar:[0,2,1,""],go_to_point:[0,2,1,""]},"mantrap.controller":{p_ahead:[1,0,0,"-"]},"mantrap.controller.p_ahead":{p_ahead_controller:[1,3,1,""]},"mantrap.environment":{social_forces:[2,0,0,"-"],trajectron:[2,0,0,"-"]},"mantrap.environment.base":{graph_based:[2,0,0,"-"],iterative:[2,0,0,"-"]},"mantrap.environment.base.graph_based":{GraphBasedEnvironment:[2,1,1,""]},"mantrap.environment.base.graph_based.GraphBasedEnvironment":{Ghost:[2,1,1,""],add_ado:[2,2,1,""],ados:[2,2,1,""],build_connected_graph:[2,2,1,""],build_connected_graph_wo_ego:[2,2,1,""],check_graph:[2,2,1,""],copy:[2,2,1,""],detach:[2,2,1,""],predict_w_controls:[2,2,1,""],predict_w_trajectory:[2,2,1,""],predict_wo_ego:[2,2,1,""],same_initial_conditions:[2,2,1,""],sanity_check:[2,2,1,""],states:[2,2,1,""],step:[2,2,1,""],step_reset:[2,2,1,""],transcribe_graph:[2,2,1,""],visualize_prediction:[2,2,1,""],visualize_prediction_wo_ego:[2,2,1,""],write_state_to_graph:[2,2,1,""]},"mantrap.environment.base.iterative":{IterativeEnvironment:[2,1,1,""]},"mantrap.environment.base.iterative.IterativeEnvironment":{ado_mode_params:[2,2,1,""]},"mantrap.environment.simplified":{kalman:[2,0,0,"-"],orca:[2,0,0,"-"],potential_field:[2,0,0,"-"]},"mantrap.environment.simplified.kalman":{KalmanEnvironment:[2,1,1,""]},"mantrap.environment.simplified.kalman.KalmanEnvironment":{add_ado:[2,2,1,""]},"mantrap.environment.simplified.orca":{ORCAEnvironment:[2,1,1,""]},"mantrap.environment.simplified.orca.ORCAEnvironment":{LineConstraint:[2,1,1,""],add_ado:[2,2,1,""]},"mantrap.environment.simplified.orca.ORCAEnvironment.LineConstraint":{direction:[2,2,1,""],point:[2,2,1,""]},"mantrap.environment.simplified.potential_field":{PotentialFieldEnvironment:[2,1,1,""]},"mantrap.environment.simplified.potential_field.PotentialFieldEnvironment":{add_ado:[2,2,1,""]},"mantrap.environment.social_forces":{SocialForcesEnvironment:[2,1,1,""]},"mantrap.environment.social_forces.SocialForcesEnvironment":{add_ado:[2,2,1,""]},"mantrap.environment.trajectron":{Trajectron:[2,1,1,""]},"mantrap.environment.trajectron.Trajectron":{add_ado:[2,2,1,""],agent_id_from_node_id:[2,2,1,""],detach:[2,2,1,""],trajectory_from_distribution:[2,2,1,""]},"mantrap.filter":{euclidean:[4,0,0,"-"],filter_module:[4,0,0,"-"],reachability:[4,0,0,"-"]},"mantrap.filter.euclidean":{EuclideanModule:[4,1,1,""]},"mantrap.filter.filter_module":{FilterModule:[4,1,1,""]},"mantrap.filter.reachability":{ReachabilityModule:[4,1,1,""]},"mantrap.modules":{acc_interact:[6,0,0,"-"],goal_norm:[6,0,0,"-"],hj_reachibility:[6,0,0,"-"],pos_interact:[6,0,0,"-"]},"mantrap.modules.acc_interact":{InteractionAccelerationModule:[6,1,1,""]},"mantrap.modules.base":{optimization_module:[6,0,0,"-"],pure_constraint:[6,0,0,"-"],pure_objective:[6,0,0,"-"]},"mantrap.modules.base.optimization_module":{OptimizationModule:[6,1,1,""]},"mantrap.modules.base.optimization_module.OptimizationModule":{compute_constraint:[6,2,1,""],compute_objective:[6,2,1,""],compute_violation:[6,2,1,""],compute_violation_internal:[6,2,1,""],constraint:[6,2,1,""],gradient:[6,2,1,""],jacobian:[6,2,1,""],objective:[6,2,1,""]},"mantrap.modules.base.pure_constraint":{PureConstraintModule:[6,1,1,""]},"mantrap.modules.base.pure_objective":{PureObjectiveModule:[6,1,1,""]},"mantrap.modules.baselines":{control_limits:[6,0,0,"-"],goal_sum:[6,0,0,"-"],min_distance:[6,0,0,"-"]},"mantrap.modules.baselines.control_limits":{ControlLimitModule:[6,1,1,""]},"mantrap.modules.baselines.goal_sum":{GoalSumModule:[6,1,1,""]},"mantrap.modules.baselines.min_distance":{MinDistanceModule:[6,1,1,""]},"mantrap.modules.goal_norm":{GoalNormModule:[6,1,1,""]},"mantrap.modules.hj_reachibility":{HJReachabilityModule:[6,1,1,""]},"mantrap.modules.pos_interact":{InteractionPositionModule:[6,1,1,""]},"mantrap.solver":{mcts:[7,0,0,"-"],sgrad:[7,0,0,"-"]},"mantrap.solver.base":{ipopt:[7,0,0,"-"],search:[7,0,0,"-"],trajopt:[7,0,0,"-"]},"mantrap.solver.base.ipopt":{IPOPTIntermediate:[7,1,1,""]},"mantrap.solver.base.ipopt.IPOPTIntermediate":{gradient:[7,2,1,""],jacobian:[7,2,1,""]},"mantrap.solver.base.search":{SearchIntermediate:[7,1,1,""]},"mantrap.solver.base.search.SearchIntermediate":{initialize:[7,2,1,""]},"mantrap.solver.base.trajopt":{TrajOptSolver:[7,1,1,""]},"mantrap.solver.base.trajopt.TrajOptSolver":{constraints:[7,2,1,""],determine_ego_controls:[7,2,1,""],initial_values:[7,2,1,""],initialize:[7,2,1,""],log_summarize:[7,2,1,""],module_defaults:[7,2,1,""],objective:[7,2,1,""],solve:[7,2,1,""],visualize_heat_map:[7,2,1,""],visualize_scenes:[7,2,1,""]},"mantrap.solver.baselines":{orca:[7,0,0,"-"],random_search:[7,0,0,"-"]},"mantrap.solver.baselines.orca":{ORCASolver:[7,1,1,""]},"mantrap.solver.baselines.orca.ORCASolver":{initial_values:[7,2,1,""],initialize:[7,2,1,""],module_defaults:[7,2,1,""]},"mantrap.solver.baselines.random_search":{RandomSearch:[7,1,1,""]},"mantrap.solver.baselines.random_search.RandomSearch":{module_defaults:[7,2,1,""]},"mantrap.solver.mcts":{MonteCarloTreeSearch:[7,1,1,""]},"mantrap.solver.mcts.MonteCarloTreeSearch":{module_defaults:[7,2,1,""]},"mantrap.solver.sgrad":{SGradSolver:[7,1,1,""]},"mantrap.solver.sgrad.SGradSolver":{module_defaults:[7,2,1,""]},"mantrap.visualization":{curves:[8,0,0,"-"],heat_map:[8,0,0,"-"],overview:[8,0,0,"-"],trajectories:[8,0,0,"-"]},"mantrap.visualization.curves":{visualize_curves:[8,3,1,""]},"mantrap.visualization.heat_map":{visualize_heat_map:[8,3,1,""]},"mantrap_evaluation.metrics":{metric_ado_effort:[3,3,1,""],metric_directness:[3,3,1,""],metric_ego_effort:[3,3,1,""],metric_minimal_distance:[3,3,1,""]},mantrap_evaluation:{metrics:[3,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function"},terms:{"0mfdwaaqbaj":2,"abstract":5,"break":[1,2],"case":[0,2,6],"catch":6,"class":[0,2,4,5,7],"default":[0,1,2],"export":5,"final":[3,7],"float":[0,1,2,3,6,7,8],"function":[0,2,3,6,7],"import":[2,4,6],"int":[0,2,3,4,6,7],"long":2,"new":[0,2],"return":[0,2,3,4,7],"short":2,"static":[0,2],"true":[2,7],"try":6,"while":[0,2,5,6,7],Being:3,For:[0,2,3,4,5,6,7],That:2,The:[0,1,2,3,4,5,6,7,8],Then:[0,2,3,5,6],Use:6,Using:[4,6],__class__:3,__debug__:7,__eq__:2,__init__:3,_comput:4,_optim:7,a_t:3,abc:[2,7],abcmeta:[2,7],abl:[0,2],about:6,abov:[0,8],abstractli:0,acc_:6,acc_interact:6,acceler:[0,1,3,5],acceleration_max:0,accord:[2,3,6,7],accordingli:2,account:[2,4,5,6,7],accumul:3,action:[0,2,7],activ:[2,6,7],actual:[2,3,4,5,6,7],adapt:[0,6],add:[2,3,6],add_ado:2,added:[2,3,5,8],adding:6,addit:[2,3],addition:[6,7,8],ado:[2,3,4,6,7],ado_grad:2,ado_id:[2,6,7],ado_kwarg:2,ado_mode_param:2,ado_st:2,ado_states_next:2,ado_trajectori:3,ado_typ:2,ados_most_important_mod:2,affect:2,after:7,afterward:[2,5],agent:[1,2,3,4,5,6,7],agent_id_from_node_id:2,agent_kwarg:0,agent_safe_dt:2,ahead:1,aka:6,algorithm:[1,7],alia:2,all:[0,2,4,5,6,7,8],allow:[0,2],along:1,alreadi:[0,5,7],also:[0,2,6,7],alter:[0,2,3],altern:1,although:6,alwai:[0,2,4],among:2,amount:[1,6,7],analysi:4,analyt:6,ani:[2,3,6],anim:8,anoth:[0,3,7],api:5,append:[0,2],appli:[0,2,5],approach:[3,5],approxim:3,area:[2,4],arg_list:2,argument:[2,3],arithmet:0,around:[0,2],assert:[2,5],assign:2,associ:[2,7],assum:[0,1,2,3,7],assumpt:[0,2,7],attent:[4,7],autograd:6,automat:3,autonom:[5,6],avoid:[2,6],awar:[2,5],back:0,backward:[4,6],bad:0,base:[1,3,5],baselin:[5,6],bash:[3,5],basic:[0,2,3],becom:6,been:[5,6,7],befor:[6,7],begin:[2,6],behav:[0,2],behavior:[2,4,5,6],behaviour:[1,2,3,5,6],being:[0,2,6,7],belong:2,below:7,berg:2,between:[0,1,2,3,4,5,6,7],beyond:4,binari:5,bodi:2,book:2,bool:[0,2,6,7],both:[0,2,6],bound:[0,8],boundari:[0,4,8],branch:5,breaking_acc:1,brew:5,broad:3,build:[0,2,3,5,6,7],build_connected_graph:[2,6],build_connected_graph_wo_ego:2,build_ghost_id:2,built:[0,2,6],cach:6,calcul:[1,3,6],call:[0,2,3,4,5,6,7],can:[0,2,3,4,5,6,7,8],cannot:[2,6],capabl:[0,3],car:0,cardin:0,carlo:5,cartesian:0,certain:[4,6],chain:2,chanc:2,chang:[0,2,4,6,7],charact:0,check:[0,2,6],check_feasibility_control:0,check_feasibility_trajectori:0,check_graph:2,checkout:5,child:[0,2,4],chmod:5,choic:8,choos:7,chose:6,chosen:[2,4,7,8],circl:0,clamp:0,clip:0,clone:5,close:[2,4,6],closer:6,closest:[1,2],cluster:2,coinbrew:5,collaps:[2,7],collect:2,collid:4,collis:2,color:0,com:5,combin:[6,7],come:2,comfort:6,command:0,compar:[0,1,2,3,6],comparison:[0,6],complet:[0,2],compliant:5,complic:6,compon:2,comput:[0,1,2,4,6,7],computation:[5,6],compute_constraint:6,compute_object:6,compute_viol:6,compute_violation_intern:6,concaten:7,condit:[2,3,6,7],config_nam:[2,7],configur:[2,7],connect:[2,3,6],constant:[0,1,2,7],constraint:[2,5,7,8],construct:2,contain:[2,7],continu:[3,6],control:[0,2,3,5,7],control_i:0,control_limit:[0,6],control_x:0,controllimitmodul:6,converg:6,convert:[0,6,8],copi:[2,3],core:[6,7],correct:[0,2,6],correctli:7,cost:6,could:4,count:2,coupl:6,creat:[0,2,3,5,7],create_environ:3,crucial:7,current:[0,1,2,3,4,7],curv:8,curvatur:7,curve_dict:8,custom:[3,5],cut:2,cyipopt:5,data:0,data_fil:6,dataset:5,date:2,deal:[2,4,7],decai:2,decreas:6,deepcopi:2,def:3,defin:[0,2,3,6,7,8],definit:[6,7],degre:1,den:2,denot:2,depend:[0,2,6,7,8],deriv:[0,2,7],describ:8,descript:2,design:4,detach:[0,2],determin:[0,1,2,3,6,7],determine_ego_control:7,determinist:2,develop:5,deviat:[2,4],dfrac:3,dict:[2,3,8],dictionari:[0,2,3,7],did:6,differ:[0,2,3],differenti:[0,2],difficult:5,dimens:[0,2,8],dimension:[0,1,2],dinesh:2,direct:[0,2,3],directli:[0,2],directori:5,discret:[1,2,3,5,8],distanc:[0,2,3,5,7],distant:2,distribut:[2,6],doe:[0,2,4,6],done:[0,2],dont:2,doubl:[5,6],doubleintegratordtag:[0,3],down:2,download:[3,5],drawn:2,drive:6,driven:5,dtagent:[0,1,2,3],dtc:1,du_i:0,du_j:0,dubin:0,due:[0,1,2,4,5,6],dure:[0,1,2,6,7],dx_du:0,dynam:[0,1,2,4,6],dynamics_scalar:0,e_a:2,each:[0,2,3,6,7],easi:3,easier:2,easili:[0,2,3,5],effect:2,effici:[0,1,3,6],effort:[0,2,3,5],ego:[2,3,4,6,7],ego_act:2,ego_control:[2,7],ego_effort:3,ego_grad:2,ego_kwarg:2,ego_next_st:2,ego_st:2,ego_state_next:2,ego_trajectori:[2,3,6],ego_typ:[2,3],either:[0,2,5,6,8],ellips:0,empti:7,enabl:0,encod:7,encount:2,end:[1,2],enforc:[2,6,7],engin:[2,5],ensur:5,entiti:2,env:[3,4,6,7],env_kwarg:2,env_typ:[2,3],enviorn:2,environ:[0,3,4,5,6,7],equal:[2,6],equat:0,equival:[2,6],especi:[0,2,6],estim:[2,7],etc:[2,7],eth:[3,5],euclidean:5,euclideanmodul:4,eval_env:7,evalu:[0,2,6,7],even:2,everi:[0,1,2,3,4,6,7],everyth:2,evolut:2,evolv:[2,5],exact:[0,2,6,7],exampl:[0,2,3],execut:[0,2],exist:0,exp:2,expand:0,expand_state_vector:0,expand_trajectori:0,expect:[3,6],explain:7,exponenti:2,express:[0,6],extern:5,fact:[0,6],factor:0,fairli:3,fals:[0,2,6,7],far:2,faster:6,feasibl:[0,5,7],fetch:5,fiction:6,field:5,figur:8,file:[5,8],file_path:8,filter:[2,5,7],filter_modul:[4,7],filtermodul:4,find:[2,7],finit:6,first:[1,2,3,6],firstli:2,five:0,fix:2,flag:[2,7],fold:2,folder:5,follow:[0,2,3,5,6,7],foo:3,forc:5,form:0,formal:2,format:7,formul:7,forward:[0,1,2,5,6,7],found:3,framework:6,free:2,from:[0,2,3,4,5,6,7],full:[0,4,7],fulli:4,fundament:0,further:[2,4,6,7],futur:[2,7],gain:0,game:6,gaussian:2,gener:[0,1,2,4,6,7],get:[2,3,6],ghost:[2,3,6],ghost_id:2,gif:8,git:5,github:5,give:6,given:[0,1,2,6,7,8],gmm:2,go_to_point:0,goad:3,goal:[2,3,5,7],goal_norm:6,goal_sum:6,goalmeanmodul:6,goalnormmodul:6,goalsummodul:6,going:[0,2,3,7],googl:2,grad:5,grad_:2,grad_wrt:6,gradient:[1,2,6,7],grant:2,graph:[5,6],graph_bas:[2,3,4,6,7],graphbasedenviron:[2,3,4,6,7],grid:[7,8],ground:[3,5],guarante:[0,2,5],gui:2,hamilton:6,handl:0,hard:[2,6,7],hardli:5,haruki:3,has:[0,2,5,6,7],has_slack:6,have:[0,2,3,5,6,7],heat:[7,8],heat_map:8,heavi:2,helbl:2,henc:[2,7],here:[0,2,6,7],herebi:2,high:[1,2],higher:6,highli:3,histori:[0,2,3],hj_reachibl:6,hjreachabilitymodul:6,hold:2,holonom:2,horizon:[0,2,4,6,7],how:[2,3,6,7],howev:[2,3,4,5,6,7],html5:8,html:5,http:[2,5],human:5,idea:[2,6,7],ident:2,identif:0,identifi:[0,2,7],ids:6,ignor:[2,4],imag:8,imaginari:0,impact:2,implement:[0,1,2,4,6,7],importantli:0,impos:2,improv:0,includ:[0,1,2,5,6],include_ego:2,increas:[2,6],independ:[0,2,3,7],index:[2,5,6,7],indic:[2,4],individu:[0,2],infeas:7,infer:0,infinit:0,inform:[0,5,6],initi:[0,2,3,7],initial_valu:7,initialis:7,input:[0,1,2,6,7],input_s:0,insid:[0,6],inspir:1,instant:0,instantli:0,instead:[0,2,6],instinct:5,integr:[2,3,5,6],integrator_doubl:0,integrator_singl:0,integratordtag:0,inter:[2,6],interact:[2,4,5,7],interactionaccelerationmodul:6,interactionpositionmodul:6,interf:[2,5],interfac:2,intermedi:0,intern:[0,2,6,7],interpol:3,intersect:4,interv:0,intrins:2,introduc:[2,3,6,7],intuit:6,invers:0,inverse_dynam:0,invert:0,ipopt:5,ipoptintermedi:7,is_robot:0,isotrop:0,iter:[0,1,5,7,8],iterativeenviron:2,its:[0,1,2,4,6,7],itself:[4,7],ivanov:[2,5],jacobi:6,jacobian:[6,7],jur:2,just:[0,2,7],just_on:7,k_speed:0,kalman:5,kalmanenviron:2,keep:[2,7],kei:[2,7],kind:4,known:2,kth:7,kwarg:[2,7],label:8,lack:5,larg:[2,6],larger:[2,6],last:[6,7],lead:[2,6],least:0,length:[0,2],less:[4,6],let:[5,8],level:[5,7],librari:[1,6],like:[0,6],limit:[0,2,6],lin:2,line:7,linear:[2,3,5],lineardtag:0,linearli:[1,3],lineconstraint:2,list:[2,4,6,7,8],local:5,log:[2,4,5,7],log_pi:2,log_summar:7,log_vari:2,look:1,loop:4,loss:[2,6],lot:[0,2,6],lower:[0,8],lpg:2,made:[0,8],mai:3,main:2,make:[0,2,5],make_controls_feas:0,make_controls_feasible_scalar:0,maneuv:1,mani:7,manner:2,manocha:2,mantrap:[0,1,2,4,6,7,8],mantrap_evalu:[3,5],map:[7,8],markovian:2,mass:0,master:5,mat:6,math:0,matric:0,matrix:[0,6],matter:6,max:[0,1,6,7],max_acceler:3,max_sim_tim:1,max_step:0,maxim:[0,1,3,4,6],mct:7,mean:[0,2,4,6],meaning:[2,3],measur:[3,6],mere:[2,4,6],met:7,method:[0,2,3,4,5,6,7],methodolog:5,meti:5,metric:5,metric_ado_effort:3,metric_direct:3,metric_ego_effort:3,metric_minimal_dist:3,middl:7,might:[0,2,6],min:[6,7],min_dist:6,min_t:6,mind:2,mindistancemodul:6,ming:2,minim:[2,3,5],miss:2,mix:2,mixtur:2,mkdir:5,modal:[2,5],mode:[2,4,7],mode_index:2,model:[0,2,3,5,6],modul:[5,7],module_default:7,molnar:2,mont:5,montecarlotreesearch:7,more:[0,1,5,6],most:[0,2],motion:[0,2],move:[2,3,6],movement:2,much:[4,6,7],mult_g:2,multi:[2,5,7],multimod:[2,5],multipl:[0,2,7],multiprocess:7,mump:5,mus:2,must:2,naiv:0,name:[2,6,7],nativ:[0,1],natur:5,navig:5,ndarrai:[2,6,7,8],nearest:1,necessari:[5,6],neg:[6,7],neglect:3,neither:2,nest:0,network:2,neural:2,nevertheless:4,next:[2,5,6],nice:0,nlp:[5,7],node:2,node_id:2,node_typ:2,nomin:2,non:[0,2,6],none:[0,1,2,3,6,7,8],nor:2,norm:5,norm_dist:6,normal:[0,3,7],now:2,nth:2,num_ado:[2,3,7],num_inter_point:3,num_mod:[2,3],num_output_mod:2,num_step:2,number:[0,2,3,4,6],numer:[0,3,6],numpi:[2,6,7,8],obj_overal:7,object:[0,2,4,5,7,8],observ:2,obstacl:[2,5],occur:[0,6],off:[0,6],omega:2,onc:[0,2,7],one:[0,2,3,6,7,8],ones:7,onli:[0,1,2,3,6,7],online_with_torch:5,open:[4,5,8],oper:0,ops:5,opt:7,optim:[1,2,3,4,7,8],optimis:[2,7],optimization_modul:6,optimizationmodul:6,optimize_spe:6,option:[2,6],orca:5,orcaenviron:[2,7],orcasolv:7,order:[0,2,3,4,5,6,7],org:5,orient:0,origin:2,other:[0,2,3,5,6,7],otherwis:[2,7],out:[2,6],output:[1,2,8],outsid:2,over:[0,2,6,7,8],overal:[0,7],overhead:[0,2],overlai:7,overlap:7,overrightarrow:3,overwritten:7,p_ahead:1,p_ahead_control:1,pa18:2,packag:[2,5,6],pair:[0,2],paradigm:0,parallel:[2,7],param:2,paramet:[0,1,2,3,4,6,7,8],part:6,pass:[0,2,6],passant:6,path:[0,1,5,8],pavon:2,pedestrian:[2,3,5,6],peopl:5,per:[1,7],perfect:[0,2,3],perform:[2,6],permit:2,permut:2,phase:1,pi_1:2,pi_g:2,pi_i:2,pick:2,pkg_config_path:5,plan:[2,4,5,6,7],pleas:5,plot:[2,7,8],plot_path_onli:7,plt:8,png:8,point:[0,1,2,3,6,7,8],polici:7,pos:6,pos_:[0,4,6],pos_and_vel_onli:0,pos_i:0,pos_interact:6,pos_t:[0,6],pos_x:0,posit:[0,1,2,3,4,5,7],possibl:[2,3,4,6,7],potenti:5,potential_field:2,potentialfieldenviron:2,pre:[0,4],preced:2,pred_horizon:2,predict:[0,2,3,6,7],predict_w_control:2,predict_w_trajectori:2,predict_wo_ego:2,pref:2,prefer:[0,1,2],prefix:5,presenc:6,prevent:4,previou:[0,2,5],previous:6,primit:7,probabilist:2,probabl:2,problem:[4,6,7],process:7,product:2,profil:1,program:[0,2],project:[0,3,5],propag:7,properti:[0,2],proport:2,provabl:6,provid:[3,7],proxi:6,pseudo:2,pseudo_wheel_dist:0,pull:2,pure:[0,1,2,5],pure_constraint:6,pure_object:6,pureconstraintmodul:6,pureobjectivemodul:6,purpos:[0,2,7],pursuit:[0,1],pypi:5,python3:5,python:[0,1,5],pythonrobot:1,pytorch:[0,1,2,6],quantifi:5,quickli:2,quit:2,radiu:[0,4],random:[2,5],random_search:7,randomli:0,randomsearch:7,rather:[0,2,6],ratio:3,reach:[4,6,7],reachability_boundari:0,reachabilitymodul:4,reachabl:[0,5],react:[0,2],reaction:[2,7],read:[2,5],readm:5,real:[0,5,7],realli:[2,3],rebuilt:2,reciproc:2,recurs:5,reduc:[0,6],refer:[1,2,4],reflect:0,regard:[2,5,6],region:6,rel:6,relat:2,remain:2,remot:5,repeat:[0,2,7],repetit:1,repositori:5,repres:[2,7],represent:[0,2],repuls:2,request:3,requir:[0,1,2,5,6,7],reset:[0,2],resolut:[7,8],respect:[0,2],result:[0,2,5,6,7],return_mor:2,return_viol:7,right:0,risk:5,robot:[0,2,3,5,6,7],roll:[0,6],roll_trajectori:0,rule:2,run:2,runtim:5,s_t:0,safe:[5,6],safeti:5,sake:2,salzmann:2,same:[0,2,7],same_initial_condit:2,sampl:[2,7],saniti:[0,2],sanity_check:[0,2],satisfi:6,save:[0,5,8],scalar:[0,1,2,7],scale:2,scenario:[0,3,5],scene:[2,3,4,6,7],schaefer:5,scope:4,score:[3,7],scratch:2,search:5,searchintermedi:7,second:3,secondli:2,see:[0,7],select:[2,4,6],separ:[0,1,2],sequenc:0,sequenti:0,seri:7,serv:6,set:[0,2,3,5,8],setup:5,sever:[0,2,7,8],sgrad:7,sgradsolv:7,shall:7,shape2d:0,shape:[2,7],share:2,shoot:7,should:[0,1,2,3,4,6,7],show:[2,8],shown:7,sigma:[2,6],sigma_a:2,sim:2,similar:[1,2],simon:5,simpl:[0,2,4],simpli:[2,5,6],simplifi:[0,2,5],simul:[0,1,2,3,4,6,7],sinc:[0,1,2,6,7],singl:[2,3,5,6,7],size:[0,3],skip:5,slack:6,slack_weight:6,small:[0,1],smallest:7,social:5,social_forc:2,socialforcesenviron:2,societi:5,soft:6,solut:[0,6,7],solv:[2,4,7],solver:[5,6],solver_kwarg:7,solver_param:7,some:[0,1,2,4,5,6,7,8],sometim:[0,2],sort:2,sourc:5,space:[0,2,7],span:7,special:5,specif:[2,7],speed:[0,1,6,7],speed_refer:1,sphinx:5,squar:7,stai:[1,2],stamp:0,standard:2,start:[0,3],state:[0,1,2,3,4,6,7],state_4:0,state_previ:0,statement:5,steer:[0,1],step:[0,1,2,3,4,6,7,8],step_reset:2,stephen:2,still:[0,5],stochast:[2,5],storag:[2,8],store:[0,2,7],str:[0,2,3,6,7,8],straight:[0,7],strictli:6,string:0,strong:6,strongli:5,structur:[2,3],subclass:2,submodul:5,subsequ:[0,2],sudden:6,suffici:6,sum:[5,7],sum_:[0,6],sum_t:3,summar:7,superclass:[4,6],support:[2,3],sure:[0,6,7],synch:6,synchron:2,system:[2,5,6,7],t_current:4,t_horizon:[2,3,4,6],t_k:7,t_plan:7,tag:[6,7],take:[2,4,5],taken:[2,4,6,7],target:[0,1],target_point:0,tau_:2,tempor:[0,2],tensor:[0,1,2,3,6,7],term:[0,2],test:[3,5],than:[0,2,6,7],thei:[0,2,3,4,6],them:[0,6],themselv:[2,6],theoret:0,therebi:[0,2,4,6],therefor:[0,1,2,3,5,6,7],thi:[0,1,2,3,4,5,6,7],third:3,thirdparti:5,thread:7,three:7,through:6,thu:6,time:[0,1,2,3,4,5,6,7],time_new:2,time_step:[0,7],togeth:[2,7,8],tool:0,torch:[0,1,2,3,6,7],toward:5,track:1,tractabl:5,trade:[0,6],trajectori:[0,2,3,4,5,6],trajectory_from_distribut:2,trajectron:5,trajopt:7,trajoptsolv:7,transcrib:2,transcribe_graph:2,transform:[0,2,3,7],travel:3,treat:[0,2],tree:[0,5],tri:6,truncat:2,truth:3,tupl:[0,2,3,7,8],twice:0,two:[0,2,3,4,7],type:[0,1,2],u_k:0,u_p:6,u_r:6,uncertainti:[0,2],unchang:2,unconstrain:7,underli:2,understand:[3,7],uni:2,unifi:[4,6],uniform:2,uniformli:2,union:[2,3],uniqu:0,unknown:[2,7],unobserv:2,unrol:0,unroll_trajectori:0,unsaf:6,unsu:6,until:[0,7],unus:[0,3,6],updat:[0,2,5,6,7],upper:[0,8],usag:3,use:[0,2,7],used:[0,2,5,7],user:[2,7],uses:[0,2,7],using:[0,1,2,3,5,6,7,8],usual:[2,3,7],util:0,v0_a:2,v0s:2,v_a:2,v_i:0,v_t:[3,6],valid:7,valu:[0,2,6,7,8],van:2,vari:[3,5],variabl:[0,5,6,7,8],variant:0,vector:[0,2,3,6,7],vehicl:0,vel_:0,vel_i:0,vel_t:0,vel_x:0,veloc:[0,2,3,4,6,7],verbos:7,veri:[0,2],version:[2,5],video:8,violat:[6,7,8],virtual:5,visual:[2,7,8],visualis:[0,5],visualize_curv:8,visualize_heat_map:[7,8],visualize_predict:2,visualize_prediction_wo_ego:2,visualize_scen:7,w_t:6,wai:[1,4,6,7],want:6,warn:5,weight:[2,6,7],well:[2,3,6,7],were:5,what:6,wheel:0,when:[0,2,4,6,7],where:6,whether:[0,2,6,7],which:[0,1,2,3,4,5,6,7],whole:[2,7],why:2,wide:2,widespread:5,width:0,wise:6,within:[0,2,3,4,7],without:[0,2,3,6],work:5,world:[0,2,5],wors:2,worst:6,would:[2,3,4,6],wouldn:3,wrapper:5,write:2,write_state_to_graph:2,x0_default:2,x_axi:2,x_i:0,x_n:0,y_axi:2,y_label:8,yet:2,you:3,z_1:2,z_i:2,z_n:2,zero:[0,2,6,7]},titles:["Agents","Controller","Environment","Evaluation","Filter Modules","mantrap","Objective and Constraint Modules","Solver","Visualisation"],titleterms:{"abstract":[0,2,4,6,7],"class":6,acceler:6,agent:0,api:3,base:[0,2,4,6,7],baselin:7,carlo:7,code:5,constraint:6,control:[1,6],dataset:3,descript:5,detail:5,discret:0,distanc:[4,6],document:5,doubl:0,driven:6,effort:6,environ:2,euclidean:4,evalu:[3,5],field:2,filter:4,forc:2,forward:4,goal:6,grad:7,graph:2,instal:5,integr:0,interact:6,ipopt:7,iter:2,kalman:2,linear:0,mantrap:[3,5],metric:3,minim:6,mode:5,modul:[4,6],mont:7,norm:6,object:6,optim:[5,6],orca:[2,7],posit:6,potenti:2,pure:6,random:7,reachabl:[4,6],run:5,safeti:6,search:7,singl:0,social:2,solver:7,sum:6,trajectori:7,trajectron:2,tree:7,visualis:8}})
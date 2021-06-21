    %%%%%%take the input file as input
    input = readcell('inputexample.txt');
    lala = input(2:end,1);
    %%%%%%calculate CST coefficients for Q3D
    [CSTu_root,CSTl_root] = CST(1,lala);
    [CSTu_tip,CSTl_tip] = CST(2,lala);
    [CSTu_kink,CSTl_kink] = CST(3,lala);
    
    %%%%%%%%write planform for Q3D and execute Q3D
    ACC.Wing.Geom = [0, 0, 0,lala{3},0;
                     0+sind(lala{5})*lala{2}+lala{3}*.25-lala{3}*lala{4}*.25, lala{2}, sind(lala{6})*lala{2},lala{3}*lala{4},0];
    ACC.Wing.inc  = 0; % Wing incidence angle (degree)
    %airfoils CST coefficients
    ACC.Wing.Airfoils   = [CSTu_root,CSTl_root;
                           CSTu_tip,CSTl_tip;
                           CSTu_kink,CSTl_kink];                   
    ACC.Wing.eta = [0;lala{23}/100;1]; %airfoils spanwise locations  
    ACC.Visc  = 1;              % 0 for inviscid and 1 for viscous analysis
    ACC.Aero.MaxIterIndex = 50;
    rho=1.225*(288.15/(288.15-6.5*lala{26}/1000))^(1+9.81/(287*-6.5)); 
    Re = rho*lala{25}*lala{3}/(17.15E-06);
    q = 0.5*rho*(lala{25}^2); %dynamic pressure
    Cl = lala{13}*9.81/(q*((lala{3}+lala{3}*lala{4})*lala{2})); %calc CL for cruise load factor (so 1 G)
    ACC.Aero.V     = lala{25} ;           % flight speed (m/s)
    ACC.Aero.rho   = rho;         % air density  (kg/m3)
    ACC.Aero.alt   = lala{26};             % flight altitude (m)
    ACC.Aero.Re    = Re;        % reynolds number (bqased on mean aerodynamic chord)
    ACC.Aero.M     = lala{25}/340;           % flight MACCh number 
    ACC.Aero.CL    = Cl;
    %%%%%%% run Q3D
    Res = Q3D_solver(ACC);
    
    CD = Res.CDwing;
    
    %%%%write file with the CD
    fiCD = fopen('CD.txt','wt');
    fprintf(fiCD, '%g', CD);
    fclose(fiCD);
    
    
    function [CSTu,CSTl] = CST(hoi,lala)
        AFcoor = readmatrix(string(lala{19+hoi})+'.dat');
        res = length(AFcoor(:,1))/2;
        Cu = zeros(res,1);
        for i = 0+1:(res)
            Cu(i) = AFcoor(i,1)^0.5 * (1-AFcoor(i,1))^1;
        end

        b05 = zeros(res,1);
        b15 = zeros(res,1);
        b25 = zeros(res,1);
        b35 = zeros(res,1);
        b45 = zeros(res,1);
        b55 = zeros(res,1);
        for i = 0+1:(res)
            b05(i) = (1-AFcoor(i,1))^5;
            b15(i) = 5*AFcoor(i,1)*((1-AFcoor(i,1))^4);
            b25(i) = 10*(AFcoor(i,1)^2)*((1-AFcoor(i,1))^3);
            b35(i) = 10*(AFcoor(i,1)^3)*((1-AFcoor(i,1))^2);
            b45(i) = 5*(AFcoor(i,1)^4)*(1-AFcoor(i,1));
            b55(i) = AFcoor(i,1)^5;
        end
        matr = [Cu.*b05, Cu.*b15, Cu.*b25, Cu.*b35, Cu.*b45, Cu.*b55];
        CSTu = transpose(lsqr(matr,AFcoor(1:res,2)));
        CSTl = transpose(lsqr(matr,AFcoor(res+1:end,2)));
    end
    
    
    %%%%%%take the input file as input
    input = readcell('inputexample.txt');
    lala = input(2:end,1);
    %%%%%%calculate CST coefficients for Q3D
    [CSTu_root,CSTl_root] = CST(1,lala);
    [CSTu_tip,CSTl_tip] = CST(2,lala);
    [CSTu_kink,CSTl_kink] = CST(3,lala);
    
    %%%%%%%%write planform for Q3D and execute Q3D
    ACC.Wing.Geom = [0, 0, 0,lala{3},0;
                     %0+sind(lala{5})*lala{2}+lala{3}*.25-lala{3}*lala{4}*.25, lala{2}*lala{23}, sind(lala{6})*lala{2}*lala{23},midAFchord,0;
                     0+sind(lala{5})*lala{2}+lala{3}*.25-lala{3}*lala{4}*.25, lala{2}, sind(lala{6})*lala{2},lala{3}*lala{4},0];
    ACC.Wing.inc  = 0; % Wing incidence angle (degree)
    %airfoils CST coefficients
    ACC.Wing.Airfoils   = [CSTu_root,CSTl_root;
                           CSTu_tip,CSTl_tip;
                           CSTu_kink,CSTl_kink];                   
    ACC.Wing.eta = [0;lala{23}/100;1];   %airfoils spanwise locations  
    ACC.Visc  = 0;              % 0 for inviscid and 1 for viscous analysis
    ACC.Aero.MaxIterIndex = 50;
    rho=1.225*(288.15/(288.15-6.5*lala{26}/1000))^(1+9.81/(287*-6.5));
    Re = rho*lala{26}*lala{3}/(17.15E-06);
    q = 0.5*rho*(lala{25}^2);%dynamic pressure
    Cl = lala{13}*lala{14}*9.81/(q*((lala{3}+lala{3}*lala{4})*lala{2})); %calc CL for max load factor
    ACC.Aero.V     = lala{25} ;           % flight speed (m/s)
    ACC.Aero.rho   = rho;         % air density  (kg/m3)
    ACC.Aero.alt   = lala{26};             % flight altitude (m)
    ACC.Aero.Re    = Re;        % reynolds number (bqased on mean aerodynamic chord)
    ACC.Aero.M     = lala{25}/340;           % flight MACCh number 
    ACC.Aero.CL    = Cl;
    %%%%%%% run Q3D
    Res = Q3D_solver(ACC);
    
    %%%%%%write .init file for EMWET
    fid = fopen( 'EMWETfile.init','wt');
    fprintf(fid, '%g %g \n',lala{13},lala{13}*0.8);
    fprintf(fid, '%g \n',lala{14});
    fprintf(fid, '%g %g %g %g \n',(lala{3}+lala{3}*lala{4})*lala{2},lala{2}*2,2,lala{19});
    fprintf(fid, '0 %s \n',lala{20});
    fprintf(fid, '%g %s \n',lala{23}/100,lala{22});
    fprintf(fid, '1 %s \n',lala{21}); 
    fprintf(fid, '%g %g %g %g %g %g \n',lala{3}, 0, 0, 0,lala{7}/100,lala{8}/100);
    %NO KINK!%fprintf(fid, '%g %g %g %g %g %g \n',wgeo(2,4), wgeo(2,1), wgeo(2,2), wgeo(2,3),x(31),x(32));
    fprintf(fid, '%g %g %g %g %g %g \n',lala{3}*lala{4}, 0+sind(lala{5})*lala{2}+lala{3}*.25-lala{3}*lala{4}*.25, lala{2}, sind(lala{6})*lala{2},lala{7}/100,lala{8}/100);
    fprintf(fid, '%g %g \n',lala{9}/100,lala{10}/100);
    fprintf(fid, '%g \n', lala{24});
    for i = lala{24}
        fprintf(fid, '%g  %g \n', lala{27+i}/100,1200);
    end
    fprintf(fid, '%g %g %g %g \n',7.2E+10,2.8E03,4.83E08,4.69E08);
    fprintf(fid, '%g %g %g %g \n',7.2E+10,2.8E03,4.83E08,4.69E08);
    fprintf(fid, '%g %g %g %g \n',7.2E+10,2.8E03,4.83E08,4.69E08);
    fprintf(fid, '%g %g %g %g \n',7.2E+10,2.8E03,4.83E08,4.69E08);
    fprintf(fid,'%g %g \n',0.96,lala{11});
    fprintf(fid,'0 \n'); %put to 0 for no printing in command window, 1 for printing
    fclose(fid);
  
    %%%%write .load file
    lfile = [Res.Wing.Yst, Res.Wing.ccl, Res.Wing.cm_c4, Res.Wing.chord];
    fia = fopen('EMWETfile.load','wt');
    %add a value to the root for more accurate results
    fprintf(fia, '%g %g %g \n', 0 , lfile(1,2)*q, lfile(1,3)*q*lfile(1,4)*lfile(1,4));
    for i = 1:length(lfile)
       fprintf(fia, '%g %g %g \n', (lfile(i,1)/lala{2}), lfile(i,2)*q, lfile(i,3)*q*lfile(i,4));
    end
    %add a value to the tip for more accurate results
    fprintf(fia, '%g %g %g \n', 1, lfile(length(lfile),2)*q, lfile(length(lfile),3)*q*lfile(length(lfile),4)*lfile(length(lfile),4));
    fclose(fia);
    
    %%%%%%run EMWET
    EMWET EMWETfile;
    %obtain wing mass
    mass = importdata('EMWETfile.weight');
    Ws = mass.data*2
    
    %%%%%%function for CST coefs
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
    
    
    
    
    
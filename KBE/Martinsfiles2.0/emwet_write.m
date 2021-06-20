% Write the input file for EMWET

namefile    =    char('b737');
MTOW        =    20820;         %[kg]
MZF         =    18600;         %[kg]
nz_max      =    2.5;   
b           =    x(-1);            %half span, [m]
cr          =    x(2,1);           %[m]
ct          =    x          
lambdai     =    x(1);   %[deg]
lambdao     =
dihed       =    radians(6);
spar_front  =    x(5,1);
spar_rear   =    x(5,2);
ftank_start =    0;    % NOT SURE ABOUT THESE
ftank_end   =    0.85;
eng_num     =    1;
eng_ypos    =    0.282;
eng_mass    =    2400;         %kg
E_al        =    7.1E10;       %N/m2
rho_al      =    2800;         %kg/m3
Ft_al       =    4.8E8;        %N/m2
Fc_al       =    4.6E8;        %N/m2
pitch_rib   =    0.5;          %[m]
eff_factor  =    0.96;             %Depend on the stringer type
Airfoil     =    'e553';    % IDK WHAT TO DO HERE
section_num =    3;
airfoil_num =    3;
bk = 4.826;


xk = bk*tan(lambdai);
ck = cr-xk+0.01;
xt = (b-bk)*tan(lambdao) + xk;
wgeo = [ 0  0  0 cr thetar;
         xk bk 0 ck thetak;
         xt b  0 ct thetat;];
     
wing_surf = cr*bk-0.5*xk*bk; 

fid = fopen( 'Fokker50test.init','wt');
fprintf(fid, '%g %g \n',MTOW,MZF);
fprintf(fid, '%g \n',nz_max);

fprintf(fid, '%g %g %g %g \n',wing_surf,span,section_num,airfoil_num);

fprintf(fid, '0 %s \n',Airfoil);
fprintf(fid, '1 %s \n',Airfoil);
fprintf(fid, '%g %g %g %g %g %g \n',cr,0,0,0,spar_front,spar_rear);
fprintf(fid, '%g %g %g %g %g %g \n',ck,0,0,bk*tan(dihed),spar_front,spar_rear);
fprintf(fid, '%g %g %g %g %g %g \n',ct,span/2*tand(sweep_le),span/2,b*tan(dihed),spar_front,spar_rear);

fprintf(fid, '%g %g \n',ftank_start,ftank_end);

fprintf(fid, '%g \n', eng_num);
fprintf(fid, '%g  %g \n', eng_ypos,eng_mass);

fprintf(fid, '%g %g %g %g \n',E_al,rho_al,Ft_al,Fc_al);
fprintf(fid, '%g %g %g %g \n',E_al,rho_al,Ft_al,Fc_al);
fprintf(fid, '%g %g %g %g \n',E_al,rho_al,Ft_al,Fc_al);
fprintf(fid, '%g %g %g %g \n',E_al,rho_al,Ft_al,Fc_al);

fprintf(fid,'%g %g \n',eff_factor,pitch_rib)
fprintf(fid,'1 \n')
fclose(fid)
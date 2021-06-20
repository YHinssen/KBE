    
function [Res] = Q3D(constants,x,wgeo,Cl,visc,CSTk)%airfoilcoors,
    %% Aerodynamic solver setting
%     rootAFu = airfoilcoors(:,1);
%     rootAFl = airfoilcoors(:,2);
%     kinkAFu = airfoilcoors(:,5);
%     kinkAFl = airfoilcoors(:,6);
%     tipAFu  = airfoilcoors(:,3);
%     tipAFl  = airfoilcoors(:,4);
    
    bk = constants(2);
    b = x(33);
    ACC.Wing.Geom = wgeo;
    % Wing incidence angle (degree)
    ACC.Wing.inc  = 0;  

    % Define airfoils
    %                    | ->     upper curve coeff.                <-|   | ->       lower curve coeff.       <-| 
    %ACC.Wing.Airfoils   = [rootAFu' rootAFl';
    %                      kinkAFu' kinkAFl';
    %                      tipAFu' tipAFl'];
    %ACC.Wing.Airfoils   = [0.2171    0.3450    0.2975    0.2685    0.2893  -0.1299   -0.2388   -0.1635   -0.0476    0.0797;
    %                      0.2171    0.3450    0.2975    0.2685    0.2893  -0.1299   -0.2388   -0.1635   -0.0476    0.0797;
    %                      0.2171    0.3450    0.2975    0.2685    0.2893  -0.1299   -0.2388   -0.1635   -0.0476    0.0797];
    
    ACC.Wing.Airfoils   = [x(5:16);
                            CSTk(1:12);
                            x(17:28)];
    
    ACC.Wing.eta = [0;(bk/b);1];  % Spanwise location of the airfoil sections

    % Viscous vs inviscid
    ACC.Visc  = visc;              % 0 for inviscid and 1 for viscous analysis
    ACC.Aero.MaxIterIndex = 50;    %Maximum number of Iteration for the
                                    %convergence of viscous calculation
    
    % Flight Condition
    ACC.Aero.V     = constants(18);            % flight speed (m/s)
    ACC.Aero.rho   = constants(19);         % air density  (kg/m3)
    ACC.Aero.alt   = constants(20);             % flight altitude (m)
    ACC.Aero.Re    = constants(21);        % reynolds number (bqased on mean aerodynamic chord)
    ACC.Aero.M     = constants(22);           % flight MACCh number 
    ACC.Aero.CL    = Cl;          % lift coefficient - comment this line to run the code for given alpha%
    %ACC.Aero.Alpha = 2;             % angle of attACCk -  comment this line to run the code for given cl 

    %lala = 'lala'
    %% 
    %tic

    Res = Q3D_solver(ACC);

    %toc
end
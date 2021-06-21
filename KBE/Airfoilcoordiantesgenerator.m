    input = readcell('inputexample.txt');
    lala = input(2:end,1);
    %%%%%%calculate CST coefficients for Q3D
    [CSTu_root,CSTl_root] = CST(1,lala);
    [CSTu_tip,CSTl_tip] = CST(2,lala);
    [CSTu_kink,CSTl_kink] = CST(3,lala);

    fic = fopen('CSTs.txt','wt');
    fprintf(fic, '%g %g %g %g %g %g %g %g %g %g %g %g \n', CSTu_root,CSTl_root);
    fprintf(fic, '%g %g %g %g %g %g %g %g %g %g %g %g \n', CSTu_tip,CSTl_tip);
    fprintf(fic, '%g %g %g %g %g %g %g %g %g %g %g %g \n', CSTu_kink,CSTl_kink);
    fclose(fic);


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
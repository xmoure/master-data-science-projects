%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% F.-Javier Heredia https://gnom.upc.edu/heredia
% Procedure uo_nn_solve
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Xtr,ytr,wo,fo,tr_acc,Xte,yte,te_acc,niter,tex]=uo_nn_solve(num_target,tr_freq,tr_seed,tr_p,te_seed,te_q,la,epsG,kmax,ils,ialmax,kmaxBLS,epsal,c1,c2,isd,sg_al0,sg_be,sg_ga,sg_emax,sg_ebest,sg_seed,icg,irc,nu)

% Input parameters:
%
% num_target : set of digits to be identified.
%    tr_freq : frequency of the digits target in the data set.
%    tr_seed : seed for the training set random generation.
%       tr_p : size of the training set.
%    te_seed : seed for the test set random generation.
%       te_q : size of the test set.
%         la : coefficient lambda of the decay factor.
%       epsG : optimality tolerance.
%       kmax : maximum number of iterations.
%        ils : line search (1 if exact, 2 if uo_BLS, 3 if uo_BLSNW32)
%     ialmax :  formula for the maximum step lenght (1 or 2).
%    kmaxBLS : maximum number of iterations of the uo_BLSNW32.
%      epsal : minimum progress in alpha, algorithm up_BLSNW32
%      c1,c2 : (WC) parameters.
%        isd : optimization algorithm.
%     sg_al0 : \alpha^{SG}_0.
%      sg_be : \beta^{SG}.
%      sg_ga : \gamma^{SG}.
%    sg_emax : e^{SGÇ_{max}.
%   sg_ebest : e^{SG}_{best}.
%    sg_seed : seed for the first random permutation of the SG.
%        icg : if 1 : CGM-FR; if 2, CGM-PR+      (useless in this project).
%        irc : re-starting condition for the CGM (useless in this project).
%         nu : parameter of the RC2 for the CGM  (useless in this project).
%
% Output parameters:
%
%    Xtr : X^{TR}.
%    ytr : y^{TR}.
%     wo : w^*.
%     fo : {\tilde L}^*.
% tr_acc : Accuracy^{TR}.
%    Xte : X^{TE}.
%    yte : y^{TE}.
% te_acc : Accuracy^{TE}.
%  niter : total number of iterations.
%    tex : total running time (see "tic" "toc" Matlab commands).
%

%Xtr= 0; ytr= 0; wo= 0; fo= 0; tr_acc= 0; Xte= 0; yte= 0; te_acc= 0; niter= 0; tex= 0;


fprintf('[uo_nn_solve] :::::::::::::::::::::::::::::::::::::::::::::::::::\n')
fprintf('[uo_nn_solve] Pattern recognition with neural networks.\n')
fprintf('[uo_nn_solve] %s\n',datetime)
fprintf('[uo_nn_solve] :::::::::::::::::::::::::::::::::::::::::::::::::::\n')

%
% Generate training data set
%
fprintf('[uo_nn_solve] Training data set generation.\n')
[Xtr, ytr] = uo_nn_dataset(tr_seed, tr_p, num_target, tr_freq);

%
% Generate test data set
%
fprintf('[uo_nn_solve] Test data set generation.\n');

[Xte, yte] = uo_nn_dataset(te_seed, te_q, num_target, 0.0);
%
% Optimization
%
fprintf('[uo_nn_solve] Optimization\n');

% Activation function
sig = @(X)          1./(1+exp(-X));
y = @(X,w) sig(w'*sig(X));

w = zeros(size(Xtr,1),1);

% Loss function
L1 = @(w) (norm(y(Xtr,w)-ytr)^2)/size(ytr,2) + (la*norm(w)^2)/2; % loss (=obj) for GM and QNM
L2 = @(w,Xds,yds) (norm(y(Xds,w)-yds)^2)/size(yds,2) + (la*norm(w)^2)/2; % loss (=obj) for SGM

% Gradient loss function
gL1 = @(w) (2*sig(Xtr)*((y(Xtr,w)-ytr).*y(Xtr,w).*(1-y(Xtr,w)))')/size(ytr,2)+la*w; % for GM and QNM
gL2 = @(w,Xds,yds) (2*sig(Xds)*((y(Xds,w)-yds).*y(Xds,w).*(1-y(Xds,w)))')/size(yds,2)+la*w; % for SGM


if isd == 1 % Gradient Method
    fprintf('GM method\n');
    tic
    [wo,niter] = uo_GM(w,L1,gL1,epsG,kmax,epsal,kmaxBLS,ialmax,c1,c2);
    fo=L1(wo);
    tex = toc;
elseif isd == 3 % QNM Method
    fprintf('Quasi Newton method\n');
    tic
    [wo,niter] = uo_QNM(w,L1,gL1,epsG,kmax,epsal,kmaxBLS,ialmax,c1,c2);
    fo=L1(wo);
    tex = toc;
elseif isd == 7 % Stochastic Gradient Method
    fprintf('SGM method\n');
    tic
    [wo, niter] = uo_SGM(w, L2, gL2, Xtr, ytr, Xte, yte, sg_al0, sg_be, sg_ga, sg_emax, sg_ebest, sg_seed);
    fo = L2(wo, Xtr, ytr);
    tex = toc;
end


% Training accuracy
%
fprintf('[uo_nn_solve] Training Accuracy.\n');
y_fit_tr = y(Xtr, wo);
tr_acc = sum(round(y_fit_tr) == ytr)/size(ytr,2)*100;



%
% Test accuracy
%
fprintf('[uo_nn_solve] Test Accuracy.\n');
y_fit_te = y(Xte, wo);
te_acc = sum(round(y_fit_te) == yte)/size(yte,2)*100;


fprintf('L* = %6.2d\n', fo);
fprintf('niter = %1.0f\n', niter);
fprintf('Train accuracy = %1.3f\n', tr_acc);
fprintf('Test accuracy = %1.3f\n', te_acc);

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% End Procedure uo_nn_solve
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

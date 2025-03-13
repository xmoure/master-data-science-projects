function [wo,niter] = uo_GM(w,f,g,epsG,kmax,epsal,kmaxBLS,ialmax,c1,c2)

k = 1; almax = 1;
wk = [w]; dk = []; alk = []; ioutk = [];

while norm(g(w)) > epsG && k < kmax 
    d = -g(w);  
    dk = [dk, d];

    %% Step line search
    if k > 1 && ialmax == 1
        almax = alk(:,k-1)*(g(wk(:,k-1))'*dk(:,k-1))/(g(wk(:,k))'*d);
    elseif k > 1 && ialmax == 2
        almax = 2*(f(wk(:,k))-f(wk(:,k-1)))/(g(wk(:,k))'*d);
    end
    
    [al, iout] = uo_BLSNW32(f,g,w,d,almax,c1,c2,kmaxBLS,epsal);
    alk = [alk, al]; ioutk = [ioutk, iout];
    
    w = w+al*d;
    wk = [wk, w];
    k = k+1;

end
niter=k;
wo = wk(:,end);
end
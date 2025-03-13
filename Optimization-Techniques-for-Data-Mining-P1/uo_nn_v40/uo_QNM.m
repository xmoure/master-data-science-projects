function [wo,niter] = uo_QNM(w,f,g,epsG,kmax,epsal,kmaxBLS,ialmax,c1,c2)

I = eye(length(w));
k = 1; almax=1;
wk = [w];  dk = []; alk = []; ioutk = [];
H = I;

while norm(g(w)) > epsG && k < kmax 
    if k>1
        sk = w-wk(:,k-1);
        yk = g(w)-g(wdiff);
        pk = 1/(yk'*sk);
        H = (I-pk*sk*yk')*H*(I-pk*yk*sk') + pk*(sk*sk');

        %% Step line search
        if ialmax == 1
            almax = alk(:,k-1)*(g(wk(:,k-1))'*dk(:,k-1))/(g(wk(:,k))'*d);
        elseif ialmax == 2
            almax = 2*(f(wk(:,k))-f(wk(:,k-1)))/(g(wk(:,k))'*d);
        end
    end
    d = -H*g(w);
    dk = [dk, d];
    if k ~= 1
        almax = 2*(f(wk(:,k))-f(wk(:,k-1)))/(g(wk(:,k))'*d);
    end
    [al, iout] = uo_BLSNW32(f,g,w,d,almax,c1,c2,kmaxBLS,epsal);
    alk = [alk, al]; ioutk = [ioutk, iout];

    wdiff = w;
    w = w+al*d;
    wk = [wk w];
    k = k+1;
   
end
niter=k;
wo = wk(:,end);
end
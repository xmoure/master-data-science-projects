function [wo, k] = uo_SGM(w, L, gL, Xtr, ytr, Xte, yte, sg_al0, sg_be, sg_ga, sg_emax, sg_ebest, sg_seed)
% returns:
% wo: optimal weights
% k: number of iterations

    % INITIALIZATION

    % set random seed
    rng(sg_seed);

    % p is the number of columns of Xtr
    p = size(Xtr, 2);

    % size of the mini-batch
    m = floor(sg_ga * p);
    k_sg_e = ceil(p/m);
    k_sg_max = sg_emax * k_sg_e;

    lte_best = Inf;
    k = 0;

    e = 0;
    s = 0;

    a_sg = 0.01*sg_al0;
    k_sg = floor(sg_be * k_sg_max);

    while e <= sg_emax && s < sg_ebest
        %P ← {p1,p2,...,pp}
        P = randperm(p);
        for i = 0:ceil((p/m) - 1) 
            % mini-batch
            S = P(i*m+1:min((i+1)*m,p));
            X_tr_s = Xtr(:, S);
            y_tr_s = ytr(S);

            % direction 
            d = -gL(w, X_tr_s, y_tr_s);
            % step size
            if k <= k_sg
                a = (1 - k/k_sg) * sg_al0 + k/k_sg * a_sg;
            else
                a = a_sg;
            end

            % update
            w = w + a * d;
            k = k + 1;
        end
        e = e + 1;
        % calculate the loss on the test data and check if it is the best
        % loss observed so far.
        lte = L(w, Xte, yte);
        % if a best loss is found update and set the optimal weight vector
        if lte < lte_best
            lte_best = lte;
            wo = w;
            s = 0;
        else 
            s = s + 1;
        end

    end
end
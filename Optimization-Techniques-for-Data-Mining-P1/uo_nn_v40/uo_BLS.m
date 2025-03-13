% [start] Alg. BLS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [al,iWout] = uo_BLS(x,d,f,g,almax,almin,rho,c1,c2)
% iWout = 0: al does not satisfy any WC
% iWout = 1: al satisfies (WC1)
% iWout = 2: al satisfies WC (WC1+WC2)
% iWout = 3: al satisfies SWC (WC1+SWC2)
% Input validation
    if iW ~= 1 && iW ~= 2
        error('iW must be 1 (WC) or 2 (SWC)');
    end

    WC1  = @(al) f(x+al*d) <= f(x)+c1*al*g(x)'*d;
    WC2  = @(al) g(x+al*d)'*d >= c2*g(x)'*d;
    SWC2 = @(al) abs(g(x+al*d)'*d) <= c2*abs(g(x)'*d);

    % Initialize step size and output variable
    al = almax;
    iWout = 0;

    while al > almin
        % Check Wolfe condition WC1
        if WC1(al)
            if iW == 1  % check WC2
                if WC2(al) 
                    iWout = 2;
                    return;
                end
                % If only WC1 is satisfied, return iWout=1
                iWout = 1;
                return;
            else % iW == 2, check SWC
                if SWC2(al)
                    iWout = 3;
                    return;
                end
            end
        end

        % Adjust the step size for the next iteration
        al = rho * al;
    end

    % If no suitable step size is found, set iWout to 0 and al to 0
    iWout = 0;
    al = 0;

end
% [end] Alg. BLS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
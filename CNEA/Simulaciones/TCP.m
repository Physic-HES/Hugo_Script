t=1/2880; p=32; pxi=rand(p,1); vxi=1*rand(p,1).*(-1).^(floor(10*rand(p,1))); it=18200;  time=zeros(it,1); Ec=zeros(it,1);
pyi=rand(p,1); vyi=1*rand(p,1).*(-1).^(floor(10*rand(p,1))); rc=zeros(p,2,p); d=zeros(p,p);
for k=1:it;
    for g=1:length(pxi);
        for h=g:length(pxi);
            rc(h,1:2,g)=[pxi(h) pyi(h)]-[pxi(g) pyi(g)];
            d(h,g)=norm(rc(h,1:2,g));
        end
    end
    for g=1:length(pxi);
        if norm([pxi(g) pyi(g)]-[0.5 0.5],inf)>0.4;
           if pyi(g)>1-0.1/3/2 && vyi(g)>0;
              j=[0 1];
              v=[vxi(g) vyi(g)]-2*([vxi(g) vyi(g)]*(j)')*j;
              vxi(g)=v(1); vyi(g)=v(2);
           else
           end
           if pyi(g)<0.1/3/2 && vyi(g)<0;
              j=[0 -1];
              v=[vxi(g) vyi(g)]-2*([vxi(g) vyi(g)]*(j)')*j;
              vxi(g)=v(1); vyi(g)=v(2);
           else
           end
           if pxi(g)<0.1/3/2 && vxi(g)<0;
              j=[-1 0];
              v=[vxi(g) vyi(g)]-2*([vxi(g) vyi(g)]*(j)')*j;
              vxi(g)=v(1); vyi(g)=v(2);
           else
           end
           if pxi(g)>1-0.1/3/2 && vxi(g)>0;
              j=[1 0];
              v=[vxi(g) vyi(g)]-2*([vxi(g) vyi(g)]*(j)')*j;
              vxi(g)=v(1); vyi(g)=v(2);
           else
           end
        else
        end
    end
        [row,col]=find(0<d & d<0.1/3);
    for r=1:length(row);
        rr=rc(row(r),1:2,col(r)); rrn=rr/norm(rr); rrnt=angle2dcm(-pi/2,0,0)*[rrn';0]; rrnt=rrnt(1:2);
        vfila=[vxi(row(r)) vyi(row(r))]; vcol=[vxi(col(r)) vyi(col(r))];
        if [vxi(row(r)) vyi(row(r))]*rrn'<0 && [vxi(col(r)) vyi(col(r))]*rrn'>0;
            v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
            vxi(col(r))=v22(1); vyi(col(r))=v22(2);
            vxi(row(r))=v11(1); vyi(row(r))=v11(2);
        elseif [vxi(row(r)) vyi(row(r))]*rrn'>0 && [vxi(col(r)) vyi(col(r))]*rrn'>0;
            if norm([vxi(col(r)) vyi(col(r))])>norm([vxi(row(r)) vyi(row(r))])
                v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
                vxi(col(r))=v22(1); vyi(col(r))=v22(2);
                vxi(row(r))=v11(1); vyi(row(r))=v11(2);
            else
            end
        elseif [vxi(row(r)) vyi(row(r))]*rrn'<0 && [vxi(col(r)) vyi(col(r))]*rrn'<0;
            if norm([vxi(row(r)) vyi(row(r))])>norm([vxi(col(r)) vyi(col(r))])
                v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
                vxi(col(r))=v22(1); vyi(col(r))=v22(2);
                vxi(row(r))=v11(1); vyi(row(r))=v11(2);
            else
            end 
        end
    end
    clear d row col
vyi=vyi-9.81*t;
pxi=pxi+vxi*t;
pyi=pyi+vyi*t-9.81*t^2;
plot(pxi,pyi,'ob','markersize',10); xlim([0 1]); ylim([0 1]); daspect([1 1 1]);
time(k,1)=k*t; Ec(k,1)=sum(0.05/2*(vxi.^2+vyi.^2)); Ep(k,1)=sum(0.05*9.81*pyi);
drawnow
end
figure; plot(time,[Ec Ep Ec+Ep]); legend E_C E_P E_M; xlim([0 (it+1)*t]); ylabel('Energia [J]'); xlabel('Tiempo [seg]');

function TCP2(p,sec)
t=1/2880; it=sec/t; m=0.03; u=6*pi*(1E-3)/m; g=9.81; time=zeros(it,1); 
Ec=zeros(it-1,1); Ep=zeros(it-1,1); rc=zeros(p,2,p); d=zeros(p,p); radio=0.1/3/2;
pxi=[rand(p,1) zeros(p,it-1)]; vxi=[1*rand(p,1).*(-1).^(floor(100*rand(p,1))) zeros(p,it-1)];
pyi=[rand(p,1) zeros(p,it-1)]; vyi=[1*rand(p,1).*(-1).^(floor(100*rand(p,1))) zeros(p,it-1)];
w=waitbar(0,'Calculando trayectotias de la simulacion...');
for k=1:it-1;
    for g=1:p;
        for h=g:p;
            rc(h,1:2,g)=[pxi(h,k) pyi(h,k)]-[pxi(g,k) pyi(g,k)];
            d(h,g)=norm(rc(h,1:2,g));
        end
    end
    for g=1:p;
        if norm([pxi(g,k) pyi(g,k)]-[0.5 0.5],inf)>0.4;
           if pyi(g,k)>1-radio && vyi(g,k)>0;
              j=[0 1];
              v=[vxi(g,k) vyi(g,k)]-2*([vxi(g,k) vyi(g,k)]*(j)')*j;
              vxi(g,k)=v(1); vyi(g,k)=v(2);
           else
           end
           if pyi(g,k)<radio && vyi(g,k)<0;
              j=[0 -1];
              v=[vxi(g,k) vyi(g,k)]-2*([vxi(g,k) vyi(g,k)]*(j)')*j;
              vxi(g,k)=v(1); vyi(g,k)=v(2);
           else
           end
           if pxi(g,k)<radio && vxi(g,k)<0;
              j=[-1 0];
              v=[vxi(g,k) vyi(g,k)]-2*([vxi(g,k) vyi(g,k)]*(j)')*j;
              vxi(g,k)=v(1); vyi(g,k)=v(2);
           else
           end
           if pxi(g,k)>1-radio && vxi(g,k)>0;
              j=[1 0];
              v=[vxi(g,k) vyi(g,k)]-2*([vxi(g,k) vyi(g,k)]*(j)')*j;
              vxi(g,k)=v(1); vyi(g,k)=v(2);
           else
           end
        else
        end
    end
        [row,col]=find(0<d & d<radio*2);
    for r=1:length(row);
        rr=rc(row(r),1:2,col(r)); rrn=rr/norm(rr); rrnt=angle2dcm(-pi/2,0,0)*[rrn';0]; rrnt=rrnt(1:2);
        vfila=[vxi(row(r),k) vyi(row(r),k)]; vcol=[vxi(col(r),k) vyi(col(r),k)];
        if [vxi(row(r),k) vyi(row(r),k)]*rrn'<0 && [vxi(col(r),k) vyi(col(r),k)]*rrn'>0;
            v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
            vxi(col(r),k)=v22(1); vyi(col(r),k)=v22(2);
            vxi(row(r),k)=v11(1); vyi(row(r),k)=v11(2);
        elseif [vxi(row(r),k) vyi(row(r),k)]*rrn'>0 && [vxi(col(r),k) vyi(col(r),k)]*rrn'>0;
            if norm([vxi(col(r),k) vyi(col(r),k)])>norm([vxi(row(r),k) vyi(row(r),k)])
                v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
                vxi(col(r),k)=v22(1); vyi(col(r),k)=v22(2);
                vxi(row(r),k)=v11(1); vyi(row(r),k)=v11(2);
            else
            end
        elseif [vxi(row(r),k) vyi(row(r),k)]*rrn'<0 && [vxi(col(r),k) vyi(col(r),k)]*rrn'<0;
            if norm([vxi(row(r),k) vyi(row(r),k)])>norm([vxi(col(r),k) vyi(col(r),k)])
                v22=vfila*rrn'*rrn+vcol*rrnt*rrnt'; v11=vcol*rrn'*rrn+vfila*rrnt*rrnt';
                vxi(col(r),k)=v22(1); vyi(col(r),k)=v22(2);
                vxi(row(r),k)=v11(1); vyi(row(r),k)=v11(2);
            else
            end 
        end
    end
    clear d row col
vxi(:,k+1)=vxi(:,k)*exp(-u*t);
vyi(:,k+1)=(g/u+vyi(:,k))*exp(-u*t)-g/u;
pxi(:,k+1)=pxi(:,k)+vxi(:,k)/u*(1-exp(-u*t));
pyi(:,k+1)=pyi(:,k)+1/u*(g/u+vyi(:,k))*(1-exp(-u*t))-g/u*t;
time(k,1)=(k-1)*t; Ec(k,1)=sum(0.05/2*(vxi(:,k).^2+vyi(:,k).^2)); Ep(k,1)=sum(m*g*pyi(:,k));
waitbar(k/(it-1));
end
close(w)
for n=1:it;
     plot(pxi(:,n),pyi(:,n),'ob','markersize',radio*600); xlim([0 1]); ylim([0 1]); daspect([1 1 1]);
     drawnow
end
close all
s=input('Repetir simulacion: ','s');
if strfind(s,'si')>0;
    close all
    for n=1:it;
        plot(pxi(:,n),pyi(:,n),'ob','markersize',radio*600); xlim([0 1]); ylim([0 1]); daspect([1 1 1]);
        drawnow
    end
else
end
figure; plot(time(1:it-1,1),[Ec Ep Ec+Ep]); legend E_C E_P E_M; xlim([0 max(time)]); ylabel('Energia [J]'); xlabel('Tiempo [seg]');
figure; plot(time(1:it-1),pxi(:,1:it-1)'); ylabel('Coordenada X [m]'); xlabel('Tiempo [s]');
figure; plot(time(1:it-1),pyi(:,1:it-1)'); ylabel('Coordenada Y [m]'); xlabel('Tiempo [s]');
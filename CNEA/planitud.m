delta=(max(dat(:,7))-min(dat(:,7)))*1000;
desviacion=std(dat(:,7));
pmax=find(dat(:,7)==max(dat(:,7)));
pmin=find(dat(:,7)==min(dat(:,7)));
disp(' ')
t=input('Indique un titulo para la medición: ','s');
disp(' ')
disp('Delta de Planitud expresado en MILIMETROS : ')
disp(' ')
disp(delta)
disp(' ')
disp('Posicion de maximo y minimo en METROS: ')
disp(' ')
disp([{''} {'X'} {'Y'} {'Z'}; {'Maximo'} {dat(pmax,5)} {dat(pmax,6)} {max(dat(:,7))}; ...
     {'Mainimo'} {dat(pmin,5)} {dat(pmin,6)} {min(dat(:,7))}])
figure
[u,v]=meshgrid(min(dat(:,5)):1/20:max(dat(:,5)),min(dat(:,6)):1/15:max(dat(:,6)));
w=griddata(dat(:,5),dat(:,6),dat(:,7),u,v);
surf(u,v,w)
title([{'Deformación de la superficie'};{t};{date}])
xlim([min(dat(:,5)) max(dat(:,5))])
ylim([min(dat(:,6)) max(dat(:,6))])
daspect([1 1 0.005])
xlabel('X [m]'); ylabel('Y [m]'); zlabel('Z [m]')
colorbar
figure
if max(dat(:,5))<max(dat(:,6))
    pcolor(v,u,w)
    title([{'Deformación de la superficie'};{t};{date}])
    hold on; plot(dat(pmax,6),dat(pmax,5),'ok'); 
    plot(dat(pmin,6),dat(pmin,5),'ok'); hold off
    xlabel('Y [m]'); ylabel('X [m]')
elseif max(dat(:,6))<max(dat(:,5))
    pcolor(u,v,w)
    title([{'Deformación de la superficie'};{t};{date}])
    hold on; plot(dat(pmax,5),dat(pmax,6),'ok'); 
    plot(dat(pmin,5),dat(pmin,6),'ok'); hold off
    xlabel('X [m]'); ylabel('Y [m]')
end
colorbar

n=input('Cantidad de nodos: ');
ap=input('Nodo de apartamiento: ');
tiemp=input('Tiempo de simulacion: ');
x0=zeros(2*n,1);
x0(ap,1)=.5;
x=zeros(2*n,1);
f=@(t,x) [x(n+1:2*n,1);(diag(-18*ones(n,1))+diag(18*ones(n-1,1),1)+diag(18*ones(n-1,1),-1)+[zeros(1,n);cat(2,cat(2,zeros(n-2,1),diag(-18*ones(n-2,1))),zeros(n-2,1));zeros(1,n)])*x(1:n,1)-0.05*diag(ones(n,1))*x(n+1:2*n,1)]; 
tspan=[0 tiemp];
sol=ode45(f,tspan,x0');
x2 = linspace(0,tiemp,30*tiemp);
y2 = deval(sol,x2);
tic;
for i=1:length(x2(1,:));
    plot(linspace(1,n,n),y2(1:n,i),'.r',linspace(1,n,n),y2(1:n,i),'-b')
    ylim([-1 1]);
    xlim([0 n+1]);
    grid on
    xlabel('Posicion')
    ylabel('Altura');
    title('Cuerda')
    drawnow
end
toc
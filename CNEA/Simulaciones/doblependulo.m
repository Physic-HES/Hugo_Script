function doblependulo(tspan,condi)
X=ode45(@ (t,y) [y(3);y(4);(-3*10*sin(y(1))-10*sin(y(1)-2*y(2))-2*sin(y(1)-y(2))*(y(4)^2+y(3)^2*cos(y(1)-y(2))))/(3-cos(2*(y(1)-y(2))));(2*sin(y(1)-y(2))*(2*(y(3)^2+10*cos(y(1)))+y(4)^2*cos(y(1)-y(2))))/(3-cos(2*(y(1)-y(2))))],tspan,condi);
x=linspace(0,tspan(2),tspan(2)*150); y=deval(X,x,[1 2])';
for j=1:length(x); 
    plot([0 cos(y(j,1)-pi/2)],[0 sin(y(j,1)-pi/2)]); daspect([1 1 1]); 
    hold on; plot([cos(y(j,1)-pi/2) cos(y(j,2)-pi/2)+cos(y(j,1)-pi/2)],[sin(y(j,1)-pi/2) sin(y(j,2)-pi/2)+sin(y(j,1)-pi/2)]);
    plot(cos(y(j,1)-pi/2),sin(y(j,1)-pi/2),'ok'); 
    plot(cos(y(j,2)-pi/2)+cos(y(j,1)-pi/2),sin(y(j,2)-pi/2)+sin(y(j,1)-pi/2),'ok');
    hold off; xlim([-1.5 1.5]*3/2); ylim([-1.5 1.5]*3/2); grid on; 
    drawnow; 
end
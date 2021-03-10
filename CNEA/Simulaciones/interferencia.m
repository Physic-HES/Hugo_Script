[x,y]=meshgrid(-20:0.5:20,-20:0.5:20);
t=0:0.1:30;
f=pi-2.2;
w=2*pi*f;
for i=1:length(t);
    z=(0.2./exp(((x-6).^2+y.^2)./300)).*cos(w*t(i)-(2*pi/2).*((x-6).^2+y.^2).^0.5)+(0.2./exp(((x+6).^2+y.^2)./300)).*cos(w*t(i)-(2*pi/2).*((x+6).^2+y.^2).^0.5);
    subplot(2,2,[1 3])
    surf(x,y,z);
    title('Emision en fase de 2 fuentes puntuales','fontsize',13)
    colormap bone
    zlim([-2 2])
    xlabel('X')
    ylabel('Y')
    zlabel('Z')
    view([1 0.6 4])
    subplot(2,2,2)
    hold on
    plot(x(1,:),2.*(z(1,:)))
    hold off
    xlabel('Plano en Y=20')
    ylabel('Intensidad de Campo [Amp Pk-Pk]')
    ylim([0 0.3])
    title('Interferometro de Young','fontsize',13)
    subplot(2,2,4)
    hold on
    plot(y(:,length(x(1,:))),2.*(z(:,length(x(1,:)))))
    hold off
    title('Interferometro de Michelson','fontsize',13)
    xlabel('Plano en X=20')
    ylabel('Intensidad de Campo [Amp Pk-Pk]')
    ylim([0 0.3])
    drawnow
    pause(t(2)/18)
end

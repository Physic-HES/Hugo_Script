disp(' ')
disp('::: DETERMINACIÓN DE PESO Y CENTRO DE MASA :::'); disp(' ');
titulo=input('Ingrese un Titulo para la medición: ','s'); disp(' ');
imshow(imread('SRyorden.bmp'))
helpdlg('El orden en el que se introducen los datos es el que se muestra en la Figura. Se comienza con celda inferior derecha, si el lado mas largo del panel esta en posicion horizontal, y se continua en sentido antihorario. Esto define ademas el sistema de referencia ya que del ponto 2 y 1 forman el EJE X y el 4 y 1 forman el EJE Y','Orden para el ingreso de datos');
%Ingreso de datos
prompt={'Celda 1: ','Celda 2: ','Celda 3: ','Celda 4: '};
name='Numeros de serie';
numlines=1;
defaultanswer={'0','0','0','0'};
options.Resize='on';
options.WindowStyle='normal';
options.Interpreter='tex';
answer=inputdlg(prompt,name,numlines,defaultanswer,options);
C(:,4)=[strread(char(answer(1,1)));strread(char(answer(2,1)));strread(char(answer(3,1)));strread(char(answer(4,1)))];
name1='Pendientes de Calibracion';
answer1=inputdlg(prompt,name1,numlines,defaultanswer,options);
C(:,1)=[strread(char(answer1(1,1)));strread(char(answer1(2,1)));strread(char(answer1(3,1)));strread(char(answer1(4,1)))];
name2='Primer Medición en microStrain';
answer2=inputdlg(prompt,name2,numlines,defaultanswer,options);
C(:,2)=[strread(char(answer2(1,1)));strread(char(answer2(2,1)));strread(char(answer2(3,1)));strread(char(answer2(4,1)))];
name3='Angulo';
prompt3={'alpha: '};
answer3=inputdlg(prompt3,name3,numlines,defaultanswer,options);
alpha=strread(char(answer3(1,1)));
name4='Segunda Medición en microStrain';
answer4=inputdlg(prompt,name4,numlines,defaultanswer,options);
C(:,3)=[strread(char(answer4(1,1)));strread(char(answer4(2,1)));strread(char(answer4(3,1)));strread(char(answer4(4,1)))];
clearvars -except C alpha titulo
%calculo de peso y centro de masa%
r=([0 0;0.712 0;0.712 1.218*2;0 1.218*2])';
rp(1,:)=r(1,:).*cos(alpha*pi/180);
rp(2,:)=r(2,:);
for i=1:4
P1(i,1)=C(i,2)/C(i,1);
end
xy1=r*P1./sum(P1);
for i=1:4
P2(i,1)=C(i,3)/C(i,1);
end
xy2=rp*P2./sum(P1);
cg=xy1;
d=xy2-xy1;
cg(3,1)=-abs(d(1,1)/sin(alpha*pi/180));
Peso_Total_kg=sum(P2);%
Centro_de_Masa_m=cg';%
%Propagacion de Errores%
r_=ones(2,4).*0.0001;
rp_(1,:)=((ones(1,4).*cos(alpha*pi/180).*0.0001).^2+(r(1,:).*sin(alpha*pi/180).*pi/180).^2).^0.5;
rp_(2,:)=r_(2,:);
P1_=(((C(:,1).^-1).*0.06).^2+(C(:,2).*(C(:,1).^-2).*0.06).^2).^0.5;
xy1_=(((ones(2,4)*P1./sum(P1)).*max(max(r_))).^2+((r*ones(4,1)./sum(P1)).*max(P1_)).^2+((r*P1./(sum(P1)^2)).*norm(P1_)).^2).^0.5;
P2_=(((C(:,1).^-1).*0.06).^2+(C(:,2).*(C(:,1).^-2).*0.06).^2).^0.5;
xy2_=(((ones(2,4)*P2./sum(P1)).*max(max(rp_))).^2+((rp*ones(4,1)./sum(P1)).*max(P2_)).^2+((rp*P2./(sum(P1)^2)).*norm(P1_)).^2).^0.5;
cg_=xy1_;
d_=((ones(2,1).*max(xy1_)).^2+(ones(2,1).*max(xy2_)).^2).^0.5;
cg_(3,1)=(((1/sin(alpha*pi/180))*d_(1,1))^2+((d(1,1)/(sin(alpha*pi/180)^2))*cos(alpha*pi/180)*pi/180*pi/180)^2)^0.5;
Error_CG=cg_';%
Error_Peso=max([max(P1_) max(P2_)]);%
%Grafico
r1=([r(1,:);r(2,:);0 0 0 0])';
cgtex1=sprintf('   X: %s \n',num2str(Centro_de_Masa_m(1),'%-4.4f'));cgtex2=sprintf('   Y: %s \n',num2str(Centro_de_Masa_m(2),'%-4.4f'));cgtex3=sprintf('   Z: %s \n',num2str(Centro_de_Masa_m(3),'%-4.3f'));
plot3(r1(:,1),r1(:,2),r1(:,3),'.r');title([{'Pocisión del Centro de Masa'};{titulo}],'fontsize',13); grid on; xlabel('X[m]'); ylabel('Y[m]'); zlabel('Z[m]'); daspect([1 1 1]); hold on; plot3(Centro_de_Masa_m(1),Centro_de_Masa_m(2),Centro_de_Masa_m(3),'.b'); text(Centro_de_Masa_m(1),Centro_de_Masa_m(2),Centro_de_Masa_m(3),[cgtex1 cgtex2 cgtex3],'VerticalAlignment','bottom','Margin',10);...
    quiver3(zeros(3,1),zeros(3,1),zeros(3,1),[1;0;0],[0;1;0],[0;0;1],0.15); [x,y,z]=ellipsoid(Centro_de_Masa_m(1),Centro_de_Masa_m(2),Centro_de_Masa_m(3),Error_CG(1),Error_CG(2),Error_CG(3)); surf(x,y,z,'edgealpha',0.1,'facealpha',0.35,'facecolor',[0 1 0]); legend('Insertos RR','Centro de Masa','Sistema de Referencia','Elipse de Error');hold off;...
    figure; surf(x*1000,y*1000,z*1000,'edgealpha',0.1,'facealpha',0.35,'facecolor',[0 1 0]); hold on; plot3(Centro_de_Masa_m(1)*1000,Centro_de_Masa_m(2)*1000,Centro_de_Masa_m(3)*1000,'.b');  title([{'Elipse de Error para el Centro de Masa Calculado'};{titulo}],'fontsize',13); grid on; xlabel('X[mm]'); ylabel('Y[mm]'); zlabel('Z[mm]');...
    daspect([1 1 1]); view(-52,76); legend('Elipse de Error','Centro de masa'); clear x y z
%Error en Porcentajes%
Error_relativo_CG=Error_CG/norm(Centro_de_Masa_m);%
Error_relativo_Peso=Error_Peso/Peso_Total_kg;%
%RESULTADOS%
disp([{titulo} {'Fecha: '} {date}])
A=[{' '} {' '} {' '} {titulo} {'Fecha: '} {date};
    {'Centro de gravedad'} {'Valor'} {'Unidad'} {' '} {'Error Absoluto'} {'Error Rolativo'};
     {'X'} {Centro_de_Masa_m(1,1)} {'m'} {'+/-'} {Error_CG(1,1)} {Error_relativo_CG(1,1)};
     {'Y'} {Centro_de_Masa_m(1,2)} {'m'} {'+/-'} {Error_CG(1,2)} {Error_relativo_CG(1,2)};
     {'Z'} {Centro_de_Masa_m(1,3)} {'m'} {'+/-'} {Error_CG(1,3)} {Error_relativo_CG(1,3)};
     {'Peso'} {Peso_Total_kg} {'kgf'} {'+/-'} {Error_Peso} {Error_relativo_Peso}];
disp('    ----------------------------------------------------------------------------------------------')
disp(A(2:6,:))
xlswrite(titulo,A);
disp('    ----------------------------------------------------------------------------------------------')
disp(' ')
clear Error_relativo_Peso Error_relativo_CG Error_Peso Error_CG cg_ d_ xy2_ P2_ xy1_ P1_ rp_ r_ d cg xy2 xy1 P1 P2 r rp i titulo r1
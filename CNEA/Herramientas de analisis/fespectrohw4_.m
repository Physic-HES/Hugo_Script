function [Mfft,rms,coef]=fespectrohw4_(x0)
disp(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::2017:')
disp('::::::::::: ANALIZADOR DE ESPECTROS LABORATORIO DE :::::::::::::::')
disp('::::::: ESTUDIOS Y ENSAYOS DE COMPONENTES ESTRUCTURALES ::::::::::')
disp(':::::::::::: COMISIÓN NACIONAL DE ENERGIA ATÓMICA ::::::::::::::::')
disp(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::by:HES:')
disp(' ')
disp(sprintf('Cantidad de datos: %g por canal',length(x0(:,1))))
disp(sprintf('Cantidad de canales: %g',length(x0(1,:))-1))
disp(sprintf('Frecuencia de muestreo: %g Hz',1/(x0(2,1)-x0(1,1))))
disp(sprintf('Tiempo total: %g seg',max(x0(:,1))))
disp(' ')
disp('PARAMETROS DE ANALISIS:')
disp(' ')
coef=(0:2:94)'; 
%x0 es la matriz que tiene tiempo en la primer columna y señales en las demas columnas
for qq=1:length(coef);
lineas2=7000;
overl=coef(qq,1);
tam=size(x0);
lineas=2^nextpow2(lineas2-1);
B=2^nextpow2(lineas+1);
vent=[{'barthannwin'};{'bartlett'};{'blackman'};{'blackmanharris'};{'bohmanwin'};...
    {'chebwin'};{'flattopwin'};{'gausswin'};{'hamming'};{'hann'};{'kaiser'};{'nuttallwin'};...
    {'parzenwin'};{'rectwin'};{'triang'};{'tukeywin'}];
disp(' ')
disp('Tipo de Ventanas Disponibles:')
disp(' ')
Lista_ventanas=[{'01'} {'Bartlett-Hann'};{'02'} {'Bartlett'};{'03'} {'Blackman'};{'04'} {'Blackman-Harris'};...
    {'05'} {'Bohman'};{'06'} {'Chebyshev'};{'07'} {'Flat Top weighted'};{'08'} {'Gaussian'};{'09'} {'Hamming'};...
    {'10'} {'Hanning'};{'11'} {'Kaiser'};{'12'} {'Nuttall'};...
    {'13'} {'Parzen'};{'14'} {'Rectangular'};{'15'} {'Triangular'};{'16'} {'Tukey'}];
disp(Lista_ventanas);
ve=10;
v=eval([char(vent(ve)) '(B);'])';
tv=char(Lista_ventanas(ve,2));
disp(' ')
disp('Tipos de Promedios Disponibles')
disp(' ')
tp1=[{'01'} {'Lineal'};{'02'} {'Peak Hold'};{'03'} {'Exponencial'}];
disp(tp1);
tprom=1;
tp=char(tp1(tprom,2));
l=[5 1000];
    Fs=1/(x0(2,1)-x0(1,1));
    f=Fs/2.*linspace(0,1,lineas);
    df=max(f)/(lineas-1);
    P=floor((length(x0(:,1))-B)/(B*((100-overl)/100)))+1;
    Mfft=f';
    disp(' ')
    disp('CONFIGURACION DEL ANALISIS: ')
    disp(' ')
    disp(sprintf('Tipo de Ventana: %s',tv))
    disp(sprintf('Tipo de Promedio: %s',tp))
    disp(sprintf('Cantidad de Promedios: %g ',P));
    disp(sprintf('% Overlap: %g',overl))
    disp(sprintf('Delta f: %g',df));
    disp(sprintf('Tamaño de Bloque: %g',B));
    disp(sprintf('Cantidad de Lineas: %g',lineas));
    disp(sprintf('Tiempo de Bloque: %g',B*1/Fs));
    disp(' ')
    p1='Si';
    if strmatch(p1,'Si')==1;
        disp('Calculated...')
        figure;
    else
    end
    Y1=zeros(2,2*lineas,tam(2));
    for j=2:tam(2);
        Y1(1,:,j-1) = 2*(sqrt(B)/norm(v))*fft(v.*(x0(1:B,j))',2*lineas)./B;
        Y1(1,1,j-1) = Y1(1,1,j-1)/2;
        Mfft(:,j)=Y1(1,1:lineas,j-1)';
        if j-1<10;
        le(j-1,:)=sprintf('Channel 0%g \n',j-1);
        else
        le(j-1,:)=sprintf('Channel %g \n',j-1);
        end
    end
    d=1;
    g(d)=max(max(abs(Mfft(floor(0.005*lineas)+1:lineas,2:j))));
    d=d+1;
    if strmatch(p1,'Si')==1;
        plot(abs(Mfft(:,1)),abs(Mfft(:,2:j)));
        legend(le); ylim([0 1.1*max(g(:))]);
        titulo=sprintf('Spectral Analysis FFT [EU:mag] - Average: %g/%g \n',1,P);
        title(titulo); xlim([0 max(f)]); 
        ylabel('EU : Mag 0-Pk'); xlabel('Frequency [Hz]'); 
        legend; grid on;
    else
        w=waitbar(0,'Calculando promedios...');
    end
        u=2;
        if P==1
            fin=B;
        else
        end
    while u<=P;
        for zz=2:tam(2);
        ini=floor((u-1)*B*((100-overl)/100))+1; 
        fin=floor(B+(u-1)*B*((100-overl)/100));
        Y1(2,:,zz-1) = 2*(sqrt(B)/norm(v))*fft(v.*(x0(ini:fin,zz))',2*lineas)./B;
        Y1(2,1,j-1) = Y1(2,1,j-1)/2;
        if tprom==1
           Y2(1,:,zz-1) = abs(Y1(1,:,zz-1))*(u-1)/u+abs(Y1(2,:,zz-1))/u;
           Y2(2,:,zz-1) = angle(Y1(1,:,zz-1))*(u-1)/u+angle(Y1(2,:,zz-1))/u;
           Mfft(:,zz)=Y2(1,1:lineas,zz-1)'.*exp(i*Y2(2,1:lineas,zz-1)');
        elseif tprom==2
           Y2(1,:,zz-1) = max([abs(Y1(1,:,zz-1));abs(Y1(2,:,zz-1))]);
           Y2(2,:,zz-1) = max([angle(Y1(1,:,zz-1));angle(Y1(2,:,zz-1))]);
           Mfft(:,zz)=Y2(1,1:lineas,zz-1)'.*exp(i*Y2(2,1:lineas,zz-1)');
        elseif tprom==3
           Y2(1,:,zz-1) = abs(Y1(1,:,zz-1))*(u-1)/u+abs(Y1(2,:,zz-1))/P;
           Y2(2,:,zz-1) = angle(Y1(1,:,zz-1))*(u-1)/u+angle(Y1(2,:,zz-1))/P;
           Mfft(:,zz)=Y2(1,1:lineas,zz-1)'.*exp(i*Y2(2,1:lineas,zz-1)');
        else
        end
        if zz-1<10
        le(zz-1,:)=sprintf('Channel 0%g \n',zz-1);
        else
        le(zz-1,:)=sprintf('Channel %g \n',zz-1);
        end
        end
        g(d)=max(max(abs(Mfft(floor(0.005*lineas)+1:lineas,2:zz))));
        d=d+1;
        if strmatch(p1,'Si')==1;
        plot(abs(Mfft(:,1)),abs(Mfft(:,2:zz)));
        legend(le); ylim([0 1.1*max(g(:))]);
        titulo=sprintf('Spectral Analysis FFT [EU:mag] - Average: %g/%g \n',u,P);
        title(titulo); xlim([0 max(f)]); 
        ylabel('EU : Mag 0-Pk'); xlabel('Frequency [Hz]'); 
        legend; grid on;
        drawnow
        else
            waitbar(u/P);
        end
        u=u+1;
    end
    if strmatch(p1,'Si')==1;
    else
        close(w);
    end
    plot(Mfft(:,1),abs(Mfft(:,2:j)));
    legend(le); ylim([0 1.1*max(g(:))]);
    titulo=sprintf('Spectral Analysis FFT [EU:mag] - Average: %g/%g \n',P,P);
    title(titulo); xlim([0 max(f)]); 
    ylabel('EU : Mag 0-Pk'); xlabel('Frequency [Hz]'); 
    legend; grid on;
    disp('Finalized')
if ischar(l)==0;
    rms=[sqrt(sum(x0(1:fin,2:tam(2)).^2))/sqrt(fin);sqrt(sum(abs(Mfft(find(Mfft(:,1)>l(1),1,'first'):find(Mfft(:,1)<l(2),1,'last'),2:j)/sqrt(2)).^2))];
elseif ischar(l)==1;
    rms=[sqrt(sum(x0(1:fin,2:tam(2)).^2))/sqrt(fin);sqrt(sum(abs(Mfft(2:length(Mfft(:,1)),2:j)/sqrt(2)).^2))];
else
end
coef(qq,2:4)=[1/45*max(abs(Mfft(:,2))) P B*((100-coef(qq,1))/100)-floor(B*((100-coef(qq,1))/100))];
end
end
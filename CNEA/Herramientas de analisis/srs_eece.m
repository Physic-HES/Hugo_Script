function SRS=srs_eece(X,Q)
EU=input('En que unidad se midieron los datos?: ','s');
damp_type4=1/(2*Q);
overl=50;
tam=size(X);
for o=1:tam(2)-1;
    le(o,:)=sprintf('Ch %02.0f',o);
end
cdf=3;
a=floor(log(length(X(:,1)))/log(cdf));
B=2^a;
if B-length(X(:,1))>=0
    a=a-1;
end
P=floor((length(X(:,1))-B)/(B*((100-overl)/100)))+1;
dt=X(2,1)-X(1,1);
Fs=1/dt;
freq_typ4=(0:Fs/(length(X(1:B,1))-1):Fs/2)';
k_typ4 = floor(log2(Fs/2)*cdf);
j_typ4 = 0:k_typ4;
step_typ4(1,1,:) = 2.^(j_typ4/cdf);
freqM=repmat(freq_typ4,1,tam(2)-1,length(j_typ4));
stepM=repmat(step_typ4,length(freq_typ4),tam(2)-1,1);
H=(stepM.^2+i*2*damp_type4*stepM.*freqM)./(stepM.^2-freqM.^2+i*2*damp_type4*stepM.*freqM);
H=[H;conj(H(sort(1:length(H(:,1)),'descend'),:,:))];
Y3=repmat(fft(X(1:B,2:tam(2))),1,1,length(j_typ4)).*H;
SRS=[permute(step_typ4,[3 2 1]) permute(max(abs(ifft(Y3,[],1)),[],1),[3 2 1])];
A1=permute(max(abs(ifft(Y3,[],1)),[],1),[3 2 1]);
req=loginterp([200 200;1000 1500;10000 1500]);
figure;
subplot(4,1,[1 3]); plot(abs(SRS(:,1)),(SRS(:,2:tam(2)))); grid on;
set(gca, 'XScale', 'log', 'YScale', 'log')
legend(le,'Location','NorthWest'); 
limy=[0 1.1*max(max(SRS(:,2:tam(2))))];
xlim([100 max(SRS(:,1))]);
ylim(limy);
titulo=sprintf('Shock Response Spectrum SRS - Quality Factor %g - Processing %3.0f %%\n',Q,1/P*100);
title(titulo);
xlabel('Frequency [Hz]'); ylabel([EU ' 0-pk']);
hold on; loglog(req(:,1),req(:,2),'--r'); hold off;
M1=max(abs(X(:,2:end)'))';
subplot(4,1,4); gr(1)=plot(X(:,1),M1);
hold on; gr(2)=plot(X(1:B,1),M1(1:B),'-r'); hold off;
grid on;
xlim([min(X(:,1)) max(X(:,1))]);
xlabel('Time [sec]'); ylabel([EU ' 0-pk']);
u=2;
subplot(4,1,[1 3]); drawnow;
while u<=P;
    ini=floor((u-1)*B*((100-overl)/100))+1;
    fin=floor(B+(u-1)*B*((100-overl)/100));
    Y3p=repmat(fft(X(ini:fin,2:tam(2))),1,1,length(j_typ4)).*H;
    A2=permute(max(abs(ifft(Y3p,[],1)),[],1),[3 2 1]);
    A1 = max(A1,A2);
    SRS=[permute(step_typ4,[3 2 1]) A1];
    subplot(4,1,[1 3]); plot(abs(SRS(:,1)),(SRS(:,2:tam(2)))); grid on;
    set(gca, 'XScale', 'log', 'YScale', 'log')
    legend(le,'Location','NorthWest'); 
    limy=[0 max([2000 1.1*max(max(SRS(:,2:tam(2))))])];
    xlim([2E2 1E4]);
    ylim(limy);
    titulo=sprintf('Shock Response Spectrum SRS - Quality Factor %g - Processing %3.0f %%\n',Q,u/P*100);
    title(titulo);
    xlabel('Frequency [Hz]'); ylabel([EU ' 0-pk']);
    hold on; loglog(req(:,1),req(:,2),'--r'); hold off;
    u=u+1;
    subplot(4,1,4); delete(gr(2));
    hold on; gr(2)=plot(X(ini:fin,1),M1(ini:fin),'-r'); hold off;
    grid on;
    xlim([min(X(:,1)) max(X(:,1))]);
    xlabel('Time [sec]'); ylabel([EU ' 0-pk']);
    subplot(4,1,[1 3]); drawnow;
end
figure; plot(abs(SRS(:,1)),(SRS(:,2:tam(2)))); grid on;
set(gca, 'XScale', 'log', 'YScale', 'log')
legend(le,'Location','NorthWest'); 
limy=[0 max([2000 1.1*max(max(SRS(:,2:tam(2))))])];
xlim([2E2 1E4]);
ylim(limy);
titulo=sprintf('Shock Response Spectrum SRS - Quality Factor %g - Processing %3.0f %%\n',Q,(u-1)/P*100);
title(titulo);
xlabel('Frequency [Hz]'); ylabel([EU ' 0-pk']);
hold on; loglog(req(:,1),req(:,2),'--r'); hold off;
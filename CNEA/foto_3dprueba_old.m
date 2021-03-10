img1=imread('IMG1.jpg');img2=imread('IMG2.jpg');
bw1=im2bw(img1); figure; imshow(bw1);bw2=im2bw(img2); figure; imshow(bw2);
centro=[800;600];
%Prosesado de Imagenes
[f,c]=find(bw1(399:658,1099:1396)==0);
negros1=[f'+398;c'+1098];
negy1=union(negros1(2,1),negros1(2,2:length(negros1(1,:))));
h=1;
for i=2:length(negros1(1,:));
    if negros1(1,i)-negros1(1,i-1)>1 || negros1(1,i)-negros1(1,i-1)<-1
        PI1(h,1:2)=[negros1(2,i-1) floor(mean(negros1(1,h:i-1)))];
        h=i;
    elseif negros1(1,i)-negros1(1,i-1)==1
        PI1(i,1:2)=[3 3];
    end
end
%otra opcion
h=400;
for i=1099:1396;
    for k=400:658;
        if bw1(k,i)-bw1(k-1,i)<0
        j1=k;
        elseif bw1(k,i)-bw1(k-1,i)>0
        j2=k;
        else
            j1=-1;j2=1;
        end
        j=[j1 j2];
        PI1(k,i)=floor(mean(j));    
    end  
end
%Prosesado de Imagenes
p1i=[1129;429];p2i=[1129;529];p3i=[1132;622];p4i=[1258;421];p5i=[1259;530];p6i=[1261;620];p7i=[1369;424];p8i=[1374;529];p9i=[1377;624];
p1d=[660;442];p2d=[661;544];p3d=[663;636];p4d=[772;437];p5d=[772;541];p6d=[774;633];p7d=[892;438];p8d=[898;543];p9d=[901;638];
piz=[p1i p2i p3i p4i p5i p6i p7i p8i p9i];pd=[p1d p2d p3d p4d p5d p6d p7d p8d p9d];
cenet=[800.*[ones(1,9)];600.*[ones(1,9)]];
coord_i=[[1 0]*(piz-cenet);[0 -1]*(piz-cenet)];coord_d=[[1 0]*(pd-cenet);[0 -1]*(pd-cenet)];
b=1600; a=0.107;
P=[(a./(coord_i(1,:)-coord_d(1,:))).*((coord_i(1,:)+coord_d(1,:))./2);...
(a./(coord_i(1,:)-coord_d(1,:))).*b;...
(a./(coord_i(1,:)-coord_d(1,:))).*b.*(coord_d(2,:)./((((coord_d(1,:)).^2+b^2).^0.5).*cos(atan(coord_d(1,:)./b))))]
figure; plot3(P(1,:),P(2,:),P(3,:),'.r')
daspect([1 1 1])
ylim([0 0.4])
xlim([-0.1 0.1])
zlim([-0.05 0.045])
grid on
xlabel('X');ylabel('Y');zlabel('Z')
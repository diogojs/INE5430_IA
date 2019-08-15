clear all
close all

Data=importfile('fashion-mnist_train.csv',2,30001);
input_train = Data(:,2:end);
target_train= Data(:,1);

Data=importfile('fashion-mnist_test.csv',2,10001);
input_test = Data(:,2:end);
target_test= Data(:,1);

clear Data;

target_string={0 'T-shirt/top';
1 'Trouser';
2 'Pullover';
3 'Dress';
4 'Coat';
5 'Sandal';
6 'Shirt';
7 'Sneaker';
8 'Bag';
9 'Ankle boot'};

perm = randperm(size(input_train, 1),20);

output_data = zeros(30000, 10);
for i=1:30000
    idx = target_train(i) + 1;
    output_data(i, idx) = 1;
end

output_test = zeros(10000, 10);
for i=1:10000
    idx = target_test(i) + 1;
    output_test(i, idx) = 1;
end

x = input_train';
t = output_data';

trainFcn = 'trainscg';  
hiddenLayerSize = [50 22];
net = newff(x, t, hiddenLayerSize, {'tansig' 'tansig'}, trainFcn);

net.divideParam.trainRatio = 80/100;
net.divideParam.valRatio = 20/100;
net.divideParam.testRatio =0 ;
net.trainParam.epochs = 200;
[net,tr] = train(net,x,t);

u =  output_test';
% Test the Network
y = net(input_test');
e = gsubtract(u,y);
performance = perform(net,u,y)
tind = vec2ind(u);
yind = vec2ind(y);
percentErrors = sum(tind ~= yind)/numel(tind);

% View the Network
view(net)

figure, plotconfusion(u,y)


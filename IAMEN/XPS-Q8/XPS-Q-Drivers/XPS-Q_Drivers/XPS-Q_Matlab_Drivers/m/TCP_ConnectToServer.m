function [ socketId ] = TCP_ConnectToServer ( IP, port, timeOut )
%TCP_ConnectToServer : Connect to server
%   This is a simple function is called to receive a socketId that is 
%   needed to run any other XPS command.

if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return
end

socketId = calllib ('XPS_Q8_drivers', 'TCP_ConnectToServer', IP, port, timeOut) ;

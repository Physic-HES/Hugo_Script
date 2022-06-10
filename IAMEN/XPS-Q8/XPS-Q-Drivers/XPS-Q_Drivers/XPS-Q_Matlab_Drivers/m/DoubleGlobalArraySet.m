function [errorCode] = DoubleGlobalArraySet(socketId, Number, DoubleValue)
%DoubleGlobalArraySet :  Set double global array value
%
%	[errorCode] = DoubleGlobalArraySet(socketId, Number, DoubleValue)
%
%	* Input parameters :
%		int32 socketId
%		int32 Number
%		double DoubleValue
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_Q8_drivers', 'DoubleGlobalArraySet', socketId, Number, DoubleValue);

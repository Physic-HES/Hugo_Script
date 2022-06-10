function [errorCode, DoubleValue] = DoubleGlobalArrayGet(socketId, Number)
%DoubleGlobalArrayGet :  Get double global array value
%
%	[errorCode, DoubleValue] = DoubleGlobalArrayGet(socketId, Number)
%
%	* Input parameters :
%		int32 socketId
%		int32 Number
%	* Output parameters :
%		int32 errorCode
%		doublePtr DoubleValue


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
DoubleValue = 0;

% lib call
[errorCode, DoubleValue] = calllib('XPS_Q8_drivers', 'DoubleGlobalArrayGet', socketId, Number, DoubleValue);

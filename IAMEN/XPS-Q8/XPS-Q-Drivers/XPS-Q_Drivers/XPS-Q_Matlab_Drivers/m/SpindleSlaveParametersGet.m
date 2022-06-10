function [errorCode, PositionerName, Ratio] = SpindleSlaveParametersGet(socketId, GroupName)
%SpindleSlaveParametersGet :  Get slave parameters
%
%	[errorCode, PositionerName, Ratio] = SpindleSlaveParametersGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerName
%		doublePtr Ratio


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerName = '';
for i = 1:103
	PositionerName = [PositionerName '          '];
end
Ratio = 0;

% lib call
[errorCode, GroupName, PositionerName, Ratio] = calllib('XPS_Q8_drivers', 'SpindleSlaveParametersGet', socketId, GroupName, PositionerName, Ratio);

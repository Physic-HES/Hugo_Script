function [errorCode] = PositionerCompensatedPCOEnable(socketId, PositionerName)
%PositionerCompensatedPCOEnable :  Enable CIE08 compensated PCO mode execution
%
%	[errorCode] = PositionerCompensatedPCOEnable(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOEnable', socketId, PositionerName);
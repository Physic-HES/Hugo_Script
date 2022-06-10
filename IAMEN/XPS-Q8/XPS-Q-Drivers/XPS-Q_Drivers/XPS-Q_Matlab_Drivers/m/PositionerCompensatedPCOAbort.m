function [errorCode] = PositionerCompensatedPCOAbort(socketId, PositionerName)
%PositionerCompensatedPCOAbort :  Abort CIE08 compensated PCO mode
%
%	[errorCode] = PositionerCompensatedPCOAbort(socketId, PositionerName)
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
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOAbort', socketId, PositionerName);

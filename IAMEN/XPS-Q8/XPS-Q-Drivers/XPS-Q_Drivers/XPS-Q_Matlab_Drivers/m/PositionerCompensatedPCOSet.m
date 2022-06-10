function [errorCode] = PositionerCompensatedPCOSet(socketId, PositionerName, Start, Stop, Distance, Width)
%PositionerCompensatedPCOSet :  Set data to CIE08 compensated PCO data buffer
%
%	[errorCode] = PositionerCompensatedPCOSet(socketId, PositionerName, Start, Stop, Distance, Width)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double Start
%		double Stop
%		double Distance
%		double Width
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOSet', socketId, PositionerName, Start, Stop, Distance, Width);

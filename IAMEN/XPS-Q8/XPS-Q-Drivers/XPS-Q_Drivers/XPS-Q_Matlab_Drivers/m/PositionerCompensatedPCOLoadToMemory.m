function [errorCode] = PositionerCompensatedPCOLoadToMemory(socketId, PositionerName, DataLines)
%PositionerCompensatedPCOLoadToMemory :  Load data lines to CIE08 compensated PCO data buffer
%
%	[errorCode] = PositionerCompensatedPCOLoadToMemory(socketId, PositionerName, DataLines)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring DataLines
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, DataLines] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOLoadToMemory', socketId, PositionerName, DataLines);

function [errorCode] = PositionerCompensatedPCOPrepare(socketId, PositionerName, ScanDirection, StartPosition)
%PositionerCompensatedPCOPrepare :  Prepare data for CIE08 compensated PCO mode
%
%	[errorCode] = PositionerCompensatedPCOPrepare(socketId, PositionerName, ScanDirection, StartPosition)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		int32 ScanDirection
%		double StartPosition
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[tmp, nbElement] = size(StartPosition);

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOPrepare', socketId, PositionerName, ScanDirection, nbElement, StartPosition);

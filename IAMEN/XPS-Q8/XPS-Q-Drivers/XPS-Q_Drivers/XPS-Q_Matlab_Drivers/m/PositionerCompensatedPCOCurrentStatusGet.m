function [errorCode, Status] = PositionerCompensatedPCOCurrentStatusGet(socketId, PositionerName)
%PositionerCompensatedPCOCurrentStatusGet :  Get current status of CIE08 compensated PCO mode
%
%	[errorCode, Status] = PositionerCompensatedPCOCurrentStatusGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr Status


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Status = 0;

% lib call
[errorCode, PositionerName, Status] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOCurrentStatusGet', socketId, PositionerName, Status);

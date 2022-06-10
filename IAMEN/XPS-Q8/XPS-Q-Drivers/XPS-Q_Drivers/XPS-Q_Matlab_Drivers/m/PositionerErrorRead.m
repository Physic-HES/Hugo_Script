function [errorCode, ErrorCode] = PositionerErrorRead(socketId, PositionerName)
%PositionerErrorRead :  Read only positioner error code without clear it
%
%	[errorCode, ErrorCode] = PositionerErrorRead(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr ErrorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ErrorCode = 0;

% lib call
[errorCode, PositionerName, ErrorCode] = calllib('XPS_Q8_drivers', 'PositionerErrorRead', socketId, PositionerName, ErrorCode);

function [errorCode, ErrorString] = ErrorStringGet(socketId, ErrorCode)
%ErrorStringGet :  Return the error string corresponding to the error code
%
%	[errorCode, ErrorString] = ErrorStringGet(socketId, ErrorCode)
%
%	* Input parameters :
%		int32 socketId
%		int32 ErrorCode
%	* Output parameters :
%		int32 errorCode
%		cstring ErrorString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ErrorString = '';
for i = 1:103
	ErrorString = [ErrorString '          '];
end

% lib call
[errorCode, ErrorString] = calllib('XPS_Q8_drivers', 'ErrorStringGet', socketId, ErrorCode, ErrorString);

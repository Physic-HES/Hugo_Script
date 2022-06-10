function [errorCode, ErrorsList] = ErrorListGet(socketId)
%ErrorListGet :  Error list
%
%	[errorCode, ErrorsList] = ErrorListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring ErrorsList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ErrorsList = '';
for i = 1:6554
	ErrorsList = [ErrorsList '          '];
end

% lib call
[errorCode, ErrorsList] = calllib('XPS_Q8_drivers', 'ErrorListGet', socketId, ErrorsList);

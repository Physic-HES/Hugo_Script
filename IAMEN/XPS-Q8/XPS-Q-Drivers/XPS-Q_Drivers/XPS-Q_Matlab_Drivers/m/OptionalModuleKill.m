function [errorCode] = OptionalModuleKill(socketId, TaskName)
%OptionalModuleKill :  Kill an optional module
%
%	[errorCode] = OptionalModuleKill(socketId, TaskName)
%
%	* Input parameters :
%		int32 socketId
%		cstring TaskName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, TaskName] = calllib('XPS_Q8_drivers', 'OptionalModuleKill', socketId, TaskName);

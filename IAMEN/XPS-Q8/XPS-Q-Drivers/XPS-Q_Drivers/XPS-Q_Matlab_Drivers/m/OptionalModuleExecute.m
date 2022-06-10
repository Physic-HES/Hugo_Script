function [errorCode] = OptionalModuleExecute(socketId, ModuleFileName)
%OptionalModuleExecute :  Execute an optional module
%
%	[errorCode] = OptionalModuleExecute(socketId, ModuleFileName)
%
%	* Input parameters :
%		int32 socketId
%		cstring ModuleFileName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, ModuleFileName] = calllib('XPS_Q8_drivers', 'OptionalModuleExecute', socketId, ModuleFileName);

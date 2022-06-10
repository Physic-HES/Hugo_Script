function [errorCode] = TCLScriptExecuteWithPriority(socketId, TCLFileName, TaskName, TaskPriorityLevel, ParametersList)
%TCLScriptExecuteWithPriority :  Execute a TCL script with defined priority
%
%	[errorCode] = TCLScriptExecuteWithPriority(socketId, TCLFileName, TaskName, TaskPriorityLevel, ParametersList)
%
%	* Input parameters :
%		int32 socketId
%		cstring TCLFileName
%		cstring TaskName
%		cstring TaskPriorityLevel
%		cstring ParametersList
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, TCLFileName, TaskName, TaskPriorityLevel, ParametersList] = calllib('XPS_Q8_drivers', 'TCLScriptExecuteWithPriority', socketId, TCLFileName, TaskName, TaskPriorityLevel, ParametersList);

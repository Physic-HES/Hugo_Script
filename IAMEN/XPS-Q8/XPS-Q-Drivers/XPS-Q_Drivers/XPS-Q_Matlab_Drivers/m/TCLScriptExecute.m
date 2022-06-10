function [errorCode] = TCLScriptExecute(socketId, TCLFileName, TaskName, ParametersList)
%TCLScriptExecute :  Execute a TCL script from a TCL file
%
%	[errorCode] = TCLScriptExecute(socketId, TCLFileName, TaskName, ParametersList)
%
%	* Input parameters :
%		int32 socketId
%		cstring TCLFileName
%		cstring TaskName
%		cstring ParametersList
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, TCLFileName, TaskName, ParametersList] = calllib('XPS_Q8_drivers', 'TCLScriptExecute', socketId, TCLFileName, TaskName, ParametersList);

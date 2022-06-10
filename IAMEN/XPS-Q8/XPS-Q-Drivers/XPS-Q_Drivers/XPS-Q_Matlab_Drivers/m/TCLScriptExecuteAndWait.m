function [errorCode, OutputParametersList] = TCLScriptExecuteAndWait(socketId, TCLFileName, TaskName, InputParametersList)
%TCLScriptExecuteAndWait :  Execute a TCL script from a TCL file and wait the end of execution to return
%
%	[errorCode, OutputParametersList] = TCLScriptExecuteAndWait(socketId, TCLFileName, TaskName, InputParametersList)
%
%	* Input parameters :
%		int32 socketId
%		cstring TCLFileName
%		cstring TaskName
%		cstring InputParametersList
%	* Output parameters :
%		int32 errorCode
%		cstring OutputParametersList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
OutputParametersList = '';
for i = 1:103
	OutputParametersList = [OutputParametersList '          '];
end

% lib call
[errorCode, TCLFileName, TaskName, InputParametersList, OutputParametersList] = calllib('XPS_Q8_drivers', 'TCLScriptExecuteAndWait', socketId, TCLFileName, TaskName, InputParametersList, OutputParametersList);

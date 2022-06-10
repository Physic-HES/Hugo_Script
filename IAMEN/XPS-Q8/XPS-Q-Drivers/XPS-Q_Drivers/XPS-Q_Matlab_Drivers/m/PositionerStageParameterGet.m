function [errorCode, ParameterValue] = PositionerStageParameterGet(socketId, PositionerName, ParameterName)
%PositionerStageParameterGet :  Return the stage parameter
%
%	[errorCode, ParameterValue] = PositionerStageParameterGet(socketId, PositionerName, ParameterName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring ParameterName
%	* Output parameters :
%		int32 errorCode
%		cstring ParameterValue


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ParameterValue = '';
for i = 1:103
	ParameterValue = [ParameterValue '          '];
end

% lib call
[errorCode, PositionerName, ParameterName, ParameterValue] = calllib('XPS_Q8_drivers', 'PositionerStageParameterGet', socketId, PositionerName, ParameterName, ParameterValue);

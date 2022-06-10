function [errorCode] = PositionerStageParameterSet(socketId, PositionerName, ParameterName, ParameterValue)
%PositionerStageParameterSet :  Save the stage parameter
%
%	[errorCode] = PositionerStageParameterSet(socketId, PositionerName, ParameterName, ParameterValue)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring ParameterName
%		cstring ParameterValue
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, ParameterName, ParameterValue] = calllib('XPS_Q8_drivers', 'PositionerStageParameterSet', socketId, PositionerName, ParameterName, ParameterValue);

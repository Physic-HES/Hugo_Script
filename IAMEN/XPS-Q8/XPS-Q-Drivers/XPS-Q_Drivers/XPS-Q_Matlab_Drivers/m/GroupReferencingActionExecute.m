function [errorCode] = GroupReferencingActionExecute(socketId, PositionerName, ReferencingAction, ReferencingSensor, ReferencingParameter)
%GroupReferencingActionExecute :  Execute an action in referencing mode
%
%	[errorCode] = GroupReferencingActionExecute(socketId, PositionerName, ReferencingAction, ReferencingSensor, ReferencingParameter)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring ReferencingAction
%		cstring ReferencingSensor
%		double ReferencingParameter
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, ReferencingAction, ReferencingSensor] = calllib('XPS_Q8_drivers', 'GroupReferencingActionExecute', socketId, PositionerName, ReferencingAction, ReferencingSensor, ReferencingParameter);
